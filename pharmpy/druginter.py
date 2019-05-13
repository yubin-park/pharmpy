import pharmpy.utils as utils
from pharmpy.rxcui import RxCUIEngine
import requests as rq
from itertools import combinations

class DrugInterEngine:

    def __init__(self, 
                root_url="http://localhost:4000/REST", 
                cache_fn="data/cache_druginter.json"):
        # "root_url" can be "https://rxnav.nlm.nih.gov/REST"
        # If you decide to use the NLM server, please be careful with 
        # the rate limit, which is 20 requests per second.
        # It is highly recommended to use RxNav-in-a-Box,
        #   a locally installable Docker container for the NLM server.
        # When the Docker container is installed, you can send requests
        # to "http://localhost:4000/REST".
        self.root_url = root_url
        self.cache_fn = cache_fn
        self.cache = utils.read_cache(self.cache_fn) # rxcui => inters
        self.rce = RxCUIEngine()
        self.session = rq.Session()

    def add_to_cache(self, pair, desc):
        rxcui_A, rxcui_B = pair[0], pair[1]
        if rxcui_A not in self.cache:
            self.cache[rxcui_A] = {}
        if rxcui_B not in self.cache[rxcui_A]:
            self.cache[rxcui_A][rxcui_B] = []
        lst_pre = self.cache[rxcui_A][rxcui_B]
        lst_pre.append(desc)
        lst_post = list(set(lst_pre))
        self.cache[rxcui_A][rxcui_B] = lst_post

    def update_cache(self, rxcui):
        # update cache
        url = "{}/interaction/interaction.json?rxcui={}&sources=ONCHigh"
        url = url.format(self.root_url, rxcui)
        r = rq.get(url)
        inter_grps = []
        if (r.status_code == rq.codes.ok and
            "interactionTypeGroup" in r.json()):
            inter_grps = r.json()["interactionTypeGroup"]
        for inter_grp in inter_grps:
            source = inter_grp["sourceName"]
            for inter_type in inter_grp["interactionType"]:
                for inter_pair in inter_type["interactionPair"]:
                    desc0 = inter_pair["description"]
                    desc = "[{}] {}".format(source, desc0)
                    pair = [x["minConceptItem"]["rxcui"] 
                            for x in inter_pair["interactionConcept"]]
                    self.add_to_cache(pair, desc)

    def lookup_cache(self, rxcui_A, rxcui_B):
        out = None
        if rxcui_A in self.cache and rxcui_B in self.cache[rxcui_A]:
            out = {"pair": [rxcui_A, rxcui_B],
                    "desc": self.cache[rxcui_A][rxcui_B]}
        return out
    
    def is_cached(self, rxcui):
        if rxcui in self.cache:
            return True
        else:
            return False

    def get_interactions_from_rxcui(self, rxcui_lst):
        rxcui_lst = list(set(rxcui_lst))
        inter_lst = []
        for rxcui_A, rxcui_B in combinations(rxcui_lst, r=2):
            if not self.is_cached(rxcui_A):
                self.update_cache(rxcui_A)
            if not self.is_cached(rxcui_B):
                self.update_cache(rxcui_B)
            out = self.lookup_cache(rxcui_A, rxcui_B)
            if out is not None:
                inter_lst.append(out)
        return inter_lst

    def get_interactions(self, ndc_lst):
        """
        Returns a list of drug-drug interactions for the given NDCs.

        Parameters
        __________
        ndc_lst: list of str
                 A list of 11-digit NDC codes.
        """

        rxcui_lst = self.rce.get_rxcui(ndc_lst)
        out = self.get_interactions_from_rxcui(rxcui_lst)
        return out

    def store_cache(self):
        utils.write_cache(self.cache, self.cache_fn)

    def run_cache(self):
        packages = utils.read_package()
        ndc_lst = list(packages.keys())
        rxcui_lst = list(set(self.rce.get_rxcui(ndc_lst)))
        for rxcui in rxcui_lst:
            self.update_cache(rxcui)
        self.store_cache()





