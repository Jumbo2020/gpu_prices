import requests
import json

API_KEY = "rpa_EGTLJ7QBY4JW5T087XQZ25IDFKZ21KFBPMLMTX2Lic6jwh"
URL = "https://api.runpod.io/graphql"

query = """
{
  gpuClouds {
    id
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

print("Status code:", response.status_code)
print("Response:", response.text)

if response.status_code == 200:
    data = response.json()
    options = data.get("data", {}).get("gpuClouds", [])
    if options:
        with open("gpu_prices.json", "w") as f:
            json.dump(options, f, indent=2)
        print("✅ Saved to gpu_prices.json")
    else:
        print("⚠️ No GPU pricing data found.")
else:
    print("❌ Failed to get data from RunPod.")
