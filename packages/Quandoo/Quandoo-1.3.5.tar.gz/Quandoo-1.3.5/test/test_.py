import unittest
import quandoo


class MyTestCase(unittest.TestCase):
    def test_prod_api(self):
        self.assertEqual(quandoo.status(), 200)

    def test_dev_api(self):
        self.assertEqual(quandoo.status_test(), 200)


if __name__ == '__main__':
    unittest.main()
