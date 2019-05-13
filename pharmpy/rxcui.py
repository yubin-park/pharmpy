import pharmpy.utils as utils
import requests as rq

class RxCUIEngine:

    def __init__(self, 
                root_url="http://localhost:4000/REST",
                cache_fn="data/cache_rxcui.json"):
        # "root_url" can be "https://rxnav.nlm.nih.gov/REST"
        # If you decide to use the NLM server, please be careful with 
        # the rate limit, which is 20 requests per second.
        # It is highly recommended to use RxNav-in-a-Box, 
        #   a locally installable Docker container for the NLM server.
        # When the Docker container is installed, you can send requests
        # to "http://localhost:4000/REST".
        self.root_url = root_url
        self.cache_fn = cache_fn
        self.cache = utils.read_cache(self.cache_fn)
        self.session = rq.Session()

    def get_rxcui(self, ndc_lst):
        """
        Returns RxCUI or a list of RxCUI for the given NDC(s).

        Parameters
        __________
        ndc_lst: list of str, or str
                 A list of 11-digit NDC codes.
        """

        output_type = "list"
        if not isinstance(ndc_lst, list):
            output_type = "value"
            ndc_lst = [ndc_lst]

        rxcui_lst = []
        for ndc in ndc_lst:
            if ndc in self.cache:
                rxcui_lst.append(self.cache[ndc])
            else:
                url = "{}/ndcstatus.json?ndc={}".format(self.root_url, ndc)
                r = self.session.get(url)
                rxcui = None
                if (r.status_code == rq.codes.ok and
                    "ndcStatus" in r.json() and
                        "rxcui" in r.json()["ndcStatus"]):
                    rxcui = r.json()["ndcStatus"]["rxcui"]
                self.cache[ndc] = rxcui
                rxcui_lst.append(rxcui)

        out = rxcui_lst
        if output_type == "value":
            out = rxcui_lst[0]

        return out

    def store_cache(self):
        utils.write_cache(self.cache, self.cache_fn)

    def run_cache(self):
        packages = utils.read_package()
        ndc_lst = list(packages.keys())
        self.get_rxcui(ndc_lst)
        self.store_cache()





