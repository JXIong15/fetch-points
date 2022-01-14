import requests

r = requests.get('http://localhost:8000/balance/')
print(r.text)
