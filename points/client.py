import requests


payer_url = 'http://localhost:8000/payer/'
tran_url = 'http://localhost:8000/transaction/'
spend_url = 'http://localhost:8000/spend/'
balance_url = 'http://localhost:8000/balance/'


# add our payers to the DB
data = {'name': "DANNON"}
r = requests.post(payer_url, data)
data = {'name': "UNILEVER"}
r = requests.post(payer_url, data)
data = {'name': "MILLER COORS"}
r = requests.post(payer_url, data)


# add our transactions
# data = {'payer': "DANNON", 'points': 1000, 'timestamp': }
# r = requests.post(payer_url, data)
# data = {'name': "UNILEVER"}
# r = requests.post(payer_url, data)
# data = {'name': "MILLER COORS"}
# r = requests.post(payer_url, data)

r = requests.get('http://localhost:8000/balance/')
print(r.text)
