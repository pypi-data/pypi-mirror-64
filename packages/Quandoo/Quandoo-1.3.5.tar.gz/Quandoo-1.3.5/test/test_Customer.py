import unittest

from quandoo.Customer import Customer
from . import agent


class MyTestCase(unittest.TestCase):
    customer_id = None

    def test_creation(self):
        customer = Customer(
            {
                'id': None,
                "firstName": 'test',
                "lastName": 'test',
                "email": 'test@mail.com',
                "phoneNumber": '+61411222333',
            },
            agent)
        print(merchant.create_reservation(customer, 2, start_qdt, extra_info=e).get_reservation())
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
