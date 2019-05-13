from pharmpy.epc import EPCEngine
import unittest

class EPCEngineTestCase(unittest.TestCase):

    def test_epc(self):

        epe = EPCEngine(digits=11)
        out = epe.get_epc("50090347201")
        self.assertEqual(out["name_proprietary"], "JANUVIA")

        out = epe.get_epc(["50090347201"])
        self.assertEqual(out[0]["name_proprietary"], "JANUVIA")

        epe = EPCEngine(digits=10)
        out = epe.get_epc("5009034721")
        self.assertEqual(out["name_proprietary"], "JANUVIA")



if __name__=="__main__":

    unittest.main()



