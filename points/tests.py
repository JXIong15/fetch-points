from django.test import TestCase
from rest_framework.test import APIClient
from .models import Payer, Transaction, Spend

client = APIClient()
root = "http://localhost:8000/"


class TestBalance(TestCase):
    def test_no_payers(self):
        resp = client.get(f'{root}balance/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, {})

    def test_with_payers(self):
        Payer.objects.create(name='ASH', total_points=100)
        Payer.objects.create(name='MISTY')
        resp = client.get(f'{root}balance/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, {'ASH': 100, 'MISTY': 0})

    def test_after_spend(self):
        payer_data = {"name": "ASH"}
        payer = client.post(f'{root}payer/', data=payer_data, format='json')
        payer_data = {"name": "MISTY"}
        client.post(f'{root}payer/', data=payer_data, format='json')

        transaction_data = {
            "payer": payer.data['name'],
            "points": 100,
            "timestamp": "2022-11-07T14:03:17Z"
        }
        client.post(f'{root}transaction/', data=transaction_data, format='json')

        spend_data = {"points": 20}
        client.post(f'{root}spend/', data=spend_data, format='json')

        resp = client.get(f'{root}balance/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, {'ASH': 80, 'MISTY': 0})


class TestPayerCreate(TestCase):
    def test_no_points(self):
        payer_data = {"name": "Ash"}
        resp = client.post(f'{root}payer/', data=payer_data)
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.data['name'], 'ASH')
        self.assertEqual(resp.data['total_points'], 0)

    def test_upper_case_name(self):
        payer_data = {"name": "Ash"}
        resp = client.post(f'{root}payer/', data=payer_data)
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.data['name'], 'ASH')

        payer_data = {"name": "misty"}
        resp = client.post(f'{root}payer/', data=payer_data)
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.data['name'], 'MISTY')

    def test_unique_name(self):
        payer_data = {"name": "MISTY"}
        client.post(f'{root}payer/', data=payer_data, format='json')
        resp = client.post(f'{root}payer/', data={'name': 'misty'}, format='json')
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.data, "MISTY name already exists. Choose a different name.")

    def test_positive_points(self):
        # tests for if an admin user wants to input positive points when creating a user
        # (not preferred because it won't be accounted for in Transactions)
        payer_data = {"name": "BROCK", "total_points": 100}
        resp = client.post(f'{root}payer/', data=payer_data, format='json')
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.data['name'], 'BROCK')
        self.assertEqual(resp.data['total_points'], 100)

    def test_negative_points(self):
        # tests for if an admin user wants to input negative points when creating a user
        # (negative values are not allowed)
        payer_data = {"name": "MISTY", "total_points": -100}
        resp = client.post(f'{root}payer/', data=payer_data, format='json')
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.data, 'Payer Points cannot be negative.')


class TestTransaction(TestCase):
    def setUp(self):
        self.payer1 = Payer.objects.create(name='ASH')
        self.payer2 = Payer.objects.create(name='MISTY')

    def test_transaction_create(self):
        transaction_data = {
            "payer": self.payer1.name,
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
            "payer": self.payer1.name,
            "points": 100,
            "timestamp": "2022-11-07T14:03:17Z"
        }
        client.post(f'{root}transaction/', data=transaction_data, format='json')
        resp = client.delete(f"{root}payer/{self.payer1.id}/", format='json')
        self.assertEqual(resp.status_code, 204)
        self.assertEqual(len(Transaction.objects.all()), 0)
        self.assertEqual(len(Payer.objects.all()), 1)

    def test_multiple_transactions_create(self):
        name = self.payer1.name
        transaction_data = {
            "payer": name,
            "points": 100,
            "timestamp": "2022-11-07T14:03:17Z"
        }
        client.post(f'{root}transaction/', data=transaction_data, format='json')
        transaction_data = {
            "payer": name,
            "points": 100,
            "timestamp": "2022-11-07T15:03:17Z"
        }
        client.post(f'{root}transaction/', data=transaction_data, format='json')
        self.assertEqual(len(Transaction.objects.all()), 2)
        self.assertEqual(Payer.objects.get(name=name).total_points, 200)

        # tests a negative transaction
        transaction_data = {
            "payer": name,
            "points": -100,
            "timestamp": "2022-11-07T16:03:17Z"
        }
        client.post(f'{root}transaction/', data=transaction_data, format='json')
        self.assertEqual(len(Transaction.objects.all()), 3)
        self.assertEqual(Transaction.objects.get(id=1).remaining_points, 0)
        self.assertEqual(Transaction.objects.get(id=2).remaining_points, 100)
        self.assertEqual(Transaction.objects.get(id=3).remaining_points, 0)
        self.assertEqual(Payer.objects.get(name=name).total_points, 100)

    def test_negative_transaction(self):
        name = self.payer1.name
        transaction_data = {
            "payer": name,
            "points": -100,
            "timestamp": "2022-11-07T15:03:17Z"
        }
        resp = client.post(f'{root}transaction/', data=transaction_data, format='json')
        self.assertEqual(resp.status_code, 400)
        payer = Payer.objects.get(name=name)
        text = f"Not enough points. {payer.name} only has {payer.total_points} points available."
        self.assertEqual(resp.data, text)
        self.assertEqual(payer.total_points, 0)


class TestSpend(TestCase):
    def setUp(self):
        self.payer1 = client.post(f'{root}payer/', data={"name": "Ash"}, format='json')
        self.payer2 = client.post(f'{root}payer/', data={"name": "Misty"}, format='json')

        transaction_data = {
            "payer": self.payer1.data['name'],
            "points": 100,
            "timestamp": "2022-11-07T14:03:17Z"
        }
        client.post(f'{root}transaction/', data=transaction_data, format='json')

    def test_normal_spend(self):
        spend_data = {"points": 20}
        resp = client.post(f'{root}spend/', data=spend_data, format='json')
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.data, [{'payer': 'ASH', 'points': -20}])

    def test_not_enough_spend(self):
        spend_data = {"points": 200}
        resp = client.post(f'{root}spend/', data=spend_data, format='json')
        self.assertEqual(resp.status_code, 400)
        text = f"Not enough points. We only have 100 available."
        self.assertEqual(resp.json(), text)

    def test_spend_oldest_points_first(self):
        transaction_data = {
            "payer": self.payer2.data['name'],
            "points": 50,
            "timestamp": "2022-10-07T14:03:17Z"
        }
        client.post(f'{root}transaction/', data=transaction_data, format='json')
        resp = client.get(f'{root}transaction/', format='json')
        self.assertEqual(resp.status_code, 200)
        # transactions are ordered by oldest timestamp
        self.assertTrue(resp.data[0]['timestamp'] < resp.data[1]['timestamp'])

        spend_data = {"points": 75}
        resp = client.post(f'{root}spend/', data=spend_data, format='json')
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.data, [
            {'payer': 'MISTY', 'points': -50},
            {'payer': 'ASH', 'points': -25}
        ])
        payer1 = Payer.objects.get(id=self.payer1.data['id'])
        payer2 = Payer.objects.get(id=self.payer2.data['id'])
        self.assertEqual(payer1.total_points, 75)
        self.assertEqual(payer2.total_points, 0)

    def test_multiple_transactions_spent(self):
        transaction_data = {
            "payer": self.payer2.data['name'],
            "points": 25,
            "timestamp": "2022-09-07T14:03:17Z"
        }
        client.post(f'{root}transaction/', data=transaction_data, format='json')
        transaction_data = {
            "payer": self.payer2.data['name'],
            "points": -20,
            "timestamp": "2022-10-07T14:03:17Z"
        }
        client.post(f'{root}transaction/', data=transaction_data, format='json')
        transaction_data = {
            "payer": self.payer1.data['name'],
            "points": 5,
            "timestamp": "2022-09-17T14:03:17Z"
        }
        client.post(f'{root}transaction/', data=transaction_data, format='json')
        client.get(f'{root}transaction/', format='json')

        # At this point: {MISTY: 5, ASH: 105}
        spend_data = {"points": 75}
        resp = client.post(f'{root}spend/', data=spend_data, format='json')
        # Based on Transaction order, MISTY's first transaction of 25 will be spent
        # {ASH: -20, ASH: 105, Spend: 50}
        # Next, ASH's 5 will be spent: {MISTY: -20, ASH: 100, Spend: 45}
        # MISTY's -20 transaction is next, meaning she and the spending power increase by 20,
        # which leaves her total_points at 0: {MISTY: 0, ASH: 100, Spend: 65}
        # Finally, the remainder is partially pulled from ASH's initial 100 transaction in the setup
        # {MISTY: 0, ASH: 35, Spend: 0}
        # From a Spend of 75, the Receipt: {MISTY: -5, ASH: -70}
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.data, [
            {'payer': 'MISTY', 'points': -5},
            {'payer': 'ASH', 'points': -70}
        ])
        payer1 = Payer.objects.get(name=self.payer1.data['name'])
        payer2 = Payer.objects.get(name=self.payer2.data['name'])
        self.assertEqual(payer1.total_points, 35)
        self.assertEqual(payer2.total_points, 0)
