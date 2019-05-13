from pharmpy.atc import ATCEngine
import unittest

class ATCEngineTestCase(unittest.TestCase):

    def test_atc(self):
        ae = ATCEngine()
        out = ae.get_atc("50090347201")
        self.assertEqual(out[0]["id"], "A10BH")
        out = ae.get_atc(["50090347201"])
        self.assertEqual(out[0][0]["id"], "A10BH")


if __name__=="__main__":

    unittest.main()



