import requests
import json

API_KEY = "rpa_EGTLJ7QBY4JW5T087XQZ25IDFKZ21KFBPMLMTX2Lic6jwh"
URL = "https://api.runpod.io/graphql"

query = """
{
  cloudComputeOptions {
    gpu
    costPerHour
    memoryInGb
    numCpus
    numGpus
    communityCloud
    secureCloud
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
    with open("gpu_prices.json", "w") as f:
        json.dump(data["data"]["cloudComputeOptions"], f, indent=2)
    print("✅ Saved to gpu_prices.json")
else:
    print(f"❌ Request failed: {response.status_code}")
    print(response.text)
