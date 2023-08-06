import unittest
from iso3_lookup import *


class MyTest(unittest.TestCase):
    def test1(self):
        self.assertEqual(get_country("AFG"), "Afghanistan")

    def test2(self):
        self.assertEqual(get_iso3("Albania"), "ALB")

    def test3(self):
        self.assertEqual(get_region("Brazil"), "Americas")


def run():
    unittest.main()


if __name__ == "__main__":
    run()
