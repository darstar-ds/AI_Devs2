import requests

url = "https://tasks.aidevs.pl/token/helloapi"
payload = {"apikey": "75798a8e-e540-4308-b6aa-5db629f93e2e"}
response = requests.post(url, json=payload)
print(response.json())