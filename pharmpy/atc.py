import pharmpy.utils as utils
from pharmpy.rxcui import RxCUIEngine
import requests as rq

class ATCEngine:

    def __init__(self, 
                root_url="http://localhost:4000/REST", 
                cache_fn="data/cache_atc.json"):
        # "root_url" can be "https://rxnav.nlm.nih.gov/REST"
        # If you decide to use the NLM server, please be careful with 
        # the rate limit, which is 20 requests per second.
        # It is highly recommended to use RxNav-in-a-Box,
        #   a locally installable Docker container for the NLM server.
        # When the Docker container is installed, you can send requests
        # to "http://localhost:4000/REST".
        self.root_url = root_url
        self.cache_fn = cache_fn
        self.cache = utils.read_cache(self.cache_fn) # rxcui => atc
        self.rce = RxCUIEngine()
        self.session = rq.Session()

    def get_atc_from_rxcui(self, rxcui_lst):

        output_type = "list"
        if not isinstance(rxcui_lst, list):
            output_type = "value"
            rxcui_lst = [rxcui_lst]

        atc_lst = []
        for rxcui in rxcui_lst:
            if rxcui in self.cache:
                atc_lst.append(self.cache[rxcui])
            else:
                url = "{}/rxclass/class/byRxcui.json?"
                url = url + "rxcui={}&relaSource=ATC"
                url = url.format(self.root_url, rxcui)
                r = self.session.get(url)
                atc = []
                if (r.status_code == rq.codes.ok and
                    "rxclassDrugInfoList" in r.json() and
                    "rxclassDrugInfo" in r.json()["rxclassDrugInfoList"]):
                    info_lst = r.json()["rxclassDrugInfoList"]
                    info = info_lst["rxclassDrugInfo"]
                    for d in info:
                        item = d["rxclassMinConceptItem"]
                        atc.append({"id": item["classId"],
                                    "name": item["className"]})
                self.cache[rxcui] = atc
                atc_lst.append(atc)
        
        out = atc_lst
        if output_type == "value":
            out = atc_lst[0]

        return out

    def get_atc(self, ndc_lst):
        """
        Returns Level-4 ATC or a list of Level-4 ATCs for the given NDC(s).

        Parameters
        __________
        ndc_lst: list of str, or str
                 A list of 11-digit NDC codes.
        """

        output_type = "list"
        if not isinstance(ndc_lst, list):
            output_type = "value"
            ndc_lst = [ndc_lst]

        rxcui_lst = self.rce.get_rxcui(ndc_lst)
        atc_lst = self.get_atc_from_rxcui(rxcui_lst)

        out = atc_lst
        if output_type == "value":
            out = atc_lst[0]

        return out

    def store_cache(self):
        utils.write_cache(self.cache, self.cache_fn)

    def run_cache(self):
        packages = utils.read_package()
        ndc_lst = list(packages.keys())
        self.get_atc(ndc_lst)
        self.store_cache()





