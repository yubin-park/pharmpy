import pharmpy.utils as utils

class EPCEngine:


    def __init__(self, digits=11):
        self.digits = digits
        self.ndc2epc = utils.read_package(digits)

    def get_epc(self, ndc_lst):
        """
        Returns EPC or a list of EPC for the given NDC(s).

        Parameters
        __________
        ndc_lst: list of str, or str
                 A list of NDC codes.
                 NDC codes can be either 10 digit standard or
                 11 digit standard based on the constructor's setting.
        """

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






