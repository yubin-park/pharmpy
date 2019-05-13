import pharmpy.utils as utils

class EPCEngine:


    def __init__(self, digits=11):
        self.digits = digits
        self.ndc2epc = utils.read_package(digits)


    def get_epc(self, ndc_lst):

        output_type = "list"
        if not isinstance(ndc_lst, list):
            output_type = "value"
            ndc_lst = [ndc_lst]

        epc_lst = []
        for ndc in ndc_lst:
            if ndc in self.ndc2epc:
                epc_lst.append(self.ndc2epc[ndc])
            else:
                epc_lst.append(None)

        out = epc_lst
        if output_type == "value":
            out = epc_lst[0]

        return out






