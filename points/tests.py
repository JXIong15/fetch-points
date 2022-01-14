from django.test import TestCase
from rest_framework.test import APIClient
from .models import Payer, Transaction, Spend

client = APIClient()
root = "http://localhost:8000/"


class TestPayerCreate(TestCase):
    def test_no_points(self):
        payer_data = {"name": "Ash"}
        resp = client.post(f'{root}payer/', data=payer_data)
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.data['name'], 'Ash')
        self.assertEqual(resp.data['total_points'], 0)

    def test_positive_points(self):
        # tests for if an admin user wants to input positive points when creating a user
        # (not preferred because it won't be accounted for in Transactions)
        payer_data = {"name": "Brock", "total_points": 100}
        resp = client.post(f'{root}payer/', data=payer_data, format='json')
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.data['name'], 'Brock')
        self.assertEqual(resp.data['total_points'], 100)

    def test_negative_points(self):
        # tests for if an admin user wants to input negative points when creating a user
        # (negative values are not allowed)
        payer_data = {"name": "Misty", "total_points": -100}
        resp = client.post(f'{root}payer/', data=payer_data, format='json')
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.data, 'Payer Points cannot be negative.')


class TestTransaction(TestCase):
    def setUp(self):
        self.payer1 = Payer.objects.create(name='Ash')
        self.payer2 = Payer.objects.create(name='Misty')

    def test_transaction_create(self):
        transaction_data = {
            "payer": self.payer1.id,
            "points": 100,
            "timestamp": "2022-11-07T14:03:17Z"
        }
        resp = client.post(f'{root}transaction/', data=transaction_data, format='json')
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.data['payer'], 1)
        self.assertEqual(resp.data['points'], 100)
        self.assertEqual(resp.data['remaining_points'], resp.data['points'])
        self.assertEqual(resp.data['timestamp'], "2022-11-07T14:03:17Z")

        # points added to user
        payer = Payer.objects.get(id=resp.data['payer'])
        self.assertEqual(payer.total_points, 100)

    def test_transaction_delete_on_cascade_from_payer(self):
        transaction_data = {
            "payer": self.payer1.id,
            "points": 100,
            "timestamp": "2022-11-07T14:03:17Z"
        }
        client.post(f'{root}transaction/', data=transaction_data, format='json')
        resp = client.delete(f"{root}payer/{self.payer1.id}/", format='json')
        self.assertEqual(resp.status_code, 204)
        self.assertEqual(len(Transaction.objects.all()), 0)
        self.assertEqual(len(Payer.objects.all()), 1)

    def test_multiple_transactions_create(self):
        payer_id = self.payer1.id
        transaction_data = {
            "payer": payer_id,
            "points": 100,
            "timestamp": "2022-11-07T14:03:17Z"
        }
        client.post(f'{root}transaction/', data=transaction_data, format='json')
        transaction_data = {
            "payer": payer_id,
            "points": 100,
            "timestamp": "2022-11-07T15:03:17Z"
        }
        client.post(f'{root}transaction/', data=transaction_data, format='json')
        self.assertEqual(len(Transaction.objects.all()), 2)
        self.assertEqual(Payer.objects.get(id=payer_id).total_points, 200)

        # tests a negative transaction
        transaction_data = {
            "payer": payer_id,
            "points": -100,
            "timestamp": "2022-11-07T15:03:17Z"
        }
        client.post(f'{root}transaction/', data=transaction_data, format='json')
        self.assertEqual(len(Transaction.objects.all()), 3)
        self.assertEqual(Payer.objects.get(id=payer_id).total_points, 100)

    def test_negative_transaction(self):
        payer_id = self.payer1.id
        transaction_data = {
            "payer": payer_id,
            "points": -100,
            "timestamp": "2022-11-07T15:03:17Z"
        }
        resp = client.post(f'{root}transaction/', data=transaction_data, format='json')
        self.assertEqual(resp.status_code, 400)
        payer = Payer.objects.get(id=payer_id)
        text = f"Not enough points. {payer.name} only has {payer.total_points} points available."
        self.assertEqual(resp.data, text)
        self.assertEqual(payer.total_points, 0)


class TestSpend(TestCase):
    pass