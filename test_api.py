import requests

url = 'http://127.0.0.1:5000/api/sample'
data = {'message': 'Hello, World!'}

response = requests.post(url, json=data)
print(response.json())
