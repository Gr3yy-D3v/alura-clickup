import requests
import json

list_id = '901105126642'
url = f"/api/v2/list/901105126642/field"

headers = {"Authorization": "1ce5770254d62b590738cee6a5ebc273e62e2f7a32c58fa02452e2fa232ae1c0"}

response = requests.get(url, headers=headers)

data = response.json()
print(data)