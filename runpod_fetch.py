import requests
import json

API_KEY = "rpa_EGTLJ7QBY4JW5T087XQZ25IDFKZ21KFBPMLMTX2Lic6jwh"
URL = "https://api.runpod.io/graphql"

query = """
{
  gpuTypes {
    id
    displayName
    memoryInGb
    maxGpuCount
    secureCloud
    communityCloud
    lowestPrice(input: {gpuCount: 1}) {
      minimumBidPrice
      uninterruptablePrice
    }
  }
}
"""

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

response = requests.post(URL, headers=headers, json={"query": query})
print("Status code:", response.status_code)
print("Response snippet:", response.text[:500])

if response.status_code == 200:
    gpu_list = response.json().get("data", {}).get("gpuTypes", [])
    if gpu_list:
        with open("gpu_prices.json", "w") as f:
            json.dump(gpu_list, f, indent=2)
        print("✅ Saved gpu_prices.json with pricing info")
    else:
        print("⚠️ No gpuTypes data found.")
else:
    print("❌ Request failed")
