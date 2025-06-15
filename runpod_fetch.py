import requests
import json

API_KEY = "rpa_EGTLJ7QBY4JW5T087XQZ25IDFKZ21KFBPMLMTX2Lic6jwh"
URL = "https://api.runpod.io/graphql"

query = """
{
  gpuTypes {
    displayName
    secureCloud
    securePrice
    nodeGroupDatacenters {
      id
      name
    }
  }
}
"""

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

response = requests.post(URL, headers=headers, json={"query": query})

if response.status_code == 200:
    data = response.json().get("data", {}).get("gpuTypes", [])
    with open("gpu_prices.json", "w") as f:
        json.dump(data, f, indent=2)
    print("✅ Saved gpu_prices.json with pricing and location info")
else:
    print(f"❌ Failed to fetch data. Status code: {response.status_code}")
    print(response.text)
