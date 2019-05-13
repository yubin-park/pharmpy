from pharmpy.druginter import DrugInterEngine
import unittest

class DrugInterEngineTestCase(unittest.TestCase):

    def test_druginter(self):
        dre = DrugInterEngine()
        out = dre.get_interactions_from_rxcui(["88014","8123"])
        self.assertEqual(out[0]["desc"][0], 
                "[ONCHigh] Triptans - monoamine oxidase (MAO) inhibitors")

if __name__=="__main__":

    unittest.main()



