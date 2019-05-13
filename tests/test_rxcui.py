from pharmpy.rxcui import RxCUIEngine
import unittest
import time

class RxCUIEngineTestCase(unittest.TestCase):

    def test_cui(self):
        rce = RxCUIEngine()
        out = rce.get_rxcui("50090347201")
        self.assertEqual(out, "665044")

        out = rce.get_rxcui(["50090347201"])
        self.assertEqual(out[0], "665044")


if __name__=="__main__":

    unittest.main()



