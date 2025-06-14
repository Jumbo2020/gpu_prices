import requests

API_KEY = "rpa_EGTLJ7QBY4JW5T087XQZ25IDFKZ21KFBPMLMTX2Lic6jwh"
URL = "https://api.runpod.io/graphql"

query = """
{
  gpuTypes {
    id
    displayName
    memoryInGb
    gpuCount
    lowCost
    secureCloud
    communityCloud
    price
    gpuDescription
  }
}
"""

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

response = requests.post(URL, headers=headers, json={"query": query})

if response.status_code == 200:
    data = response.json()
    for gpu in data["data"]["gpuTypes"]:
        print(f"Name: {gpu['displayName']}")
        print(f"Price ($/hr): {gpu['lowCost']}")
        print("-" * 30)
else:
    print(f"Request failed: {response.status_code}")
    print(response.text)
