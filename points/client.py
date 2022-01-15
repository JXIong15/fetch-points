import requests

payer_url = 'http://localhost:8000/payer/'
tran_url = 'http://localhost:8000/transaction/'
spend_url = 'http://localhost:8000/spend/'
balance_url = 'http://localhost:8000/balance/'


r = requests.get(balance_url)
print(f'Balance of empty database:\n{r.text}\n')


# add our payers to the DB
data = {'name': "DANNON"}
requests.post(payer_url, json=data)
data = {'name': "UNILEVER"}
requests.post(payer_url, json=data)
data = {'name': "MILLER COORS"}
requests.post(payer_url, json=data)
r = requests.get(payer_url)
print(f'All Payers:\n{r.text}\n')

r = requests.get(balance_url)
print(f'Balance of newly added payers:\n{r.text}\n')


# add our transactions
data = {'payer': "DANNON", 'points': 1000, 'timestamp': "2020-11-02T14:00:00Z"}
requests.post(tran_url, json=data)
data = {'payer': "UNILEVER", 'points': 200, 'timestamp': "2020-10-31T11:00:00Z"}
requests.post(tran_url, json=data)
data = {'payer': "DANNON", 'points': -200, 'timestamp': "2020-10-31T15:00:00Z"}
requests.post(tran_url, json=data)
data = {'payer': "MILLER COORS", 'points': 10000, 'timestamp': "2020-11-01T14:00:00Z"}
requests.post(tran_url, json=data)
data = {'payer': "DANNON", 'points': 300, 'timestamp': "2020-10-31T10:00:00Z"}
requests.post(tran_url, json=data)
r = requests.get(tran_url)
print(f'All Transactions (in order of oldest timestamp):\n{r.text}\n')

r = requests.get(balance_url)
print(f'Balance of payers after all transactions are run:\n{r.text}\n')


# spend some points
data = {'points': 5000}
r = requests.post(spend_url, json=data)
print(f'Spend post result:\n{r.text}\n')


# balance of payers after spend
r = requests.get(balance_url)
print('Current Balance after Spend request:')
print(r.text)
