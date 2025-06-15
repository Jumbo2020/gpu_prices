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
    securePrice
    communityPrice
    communitySpotPrice
    secureSpotPrice
    clusterPrice
    oneWeekPrice
    oneMonthPrice
    threeMonthPrice
    sixMonthPrice
  }
}
"""

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

response = requests.post(URL, headers=headers, json={"query": query})

print("Status code:", response.status_code)
print("Response snippet:", response.text[:300])

if response.status_code == 200:
    data = response.json().get("data", {}).get("gpuTypes", [])
    if data:
        with open("gpu_prices.json", "w") as f:
            json.dump(data, f, indent=2)
        print("✅ Saved gpu_prices.json with full pricing info")
    else:
        print("⚠️ No GPU pricing data found in response.")
else:
    print("❌ Failed to fetch data from RunPod API")
