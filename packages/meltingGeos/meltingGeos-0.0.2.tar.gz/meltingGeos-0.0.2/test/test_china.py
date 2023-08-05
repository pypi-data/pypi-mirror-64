import sys, os, unittest
sys.path.append(os.path.abspath("./"))
sys.path.append(os.path.abspath("../"))
from libgs import Geos


class TestChina(unittest.TestCase):

    def test_Provinces(self):
        res = Geos().search("北京", depth=1)
        self.assertEqual(res[0].name, '北京市')

if __name__ == '__main__':
    unittest.main()