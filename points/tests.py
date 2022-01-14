from django.test import TestCase
from .models import Payer, Transaction, Spend
from .serializers import PayerSerializer, TransactionSerializer, SpendSerializer


root = "http://localhost:8000/"

# Create your tests here.
class TestPayer(TestCase):
    def test_payer_create(self):
        payer_data = {"name": "Ash"}
        resp = self.client.post(root + "payer/", data=payer_data)
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.data['name'], 'Ash')
        self.assertEqual(resp.data['total_points'], 0)

        # tests for if an admin user wants to input positive points when creating a user
        # (not preferred because it won't be accounted for in Transactions)
        payer_data = {"name": "Brock", "total_points": 100}
        resp = self.client.post(root + "payer/", data=payer_data)
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.data['name'], 'Brock')
        self.assertEqual(resp.data['total_points'], 100)

        # tests for if an admin user wants to input negative points when creating a user
        # (negative values are not allowed)
        payer_data = {"name": "Misty", "total_points": -100}
        resp = self.client.post(root + "payer/", data=payer_data)
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.data, 'Payer Points cannot be negative.')


class TestTransaction(TestCase):
    def setUp(self):
        payer1 =


    def test_transaction_create(self):
        transaction_data = {
            "payer": 1,
            "points": 100,
            "timestamp": "2022-11-07T14:03:17Z"
        }
        resp = self.client.post(root + "transaction/", data=transaction_data)
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.data['name'], 'Brock')
        self.assertEqual(resp.data['total_points'], 100)


