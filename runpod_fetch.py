import requests
import json
import os

# Get the API key from the environment variable
API_KEY = os.getenv("RUNPOD_KEY")

if not API_KEY:
    print("❌ Error: RUNPOD_KEY environment variable not set.")
    exit()

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

try:
    response = requests.post(URL, headers=headers, json={"query": query})
    response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)

    data = response.json().get("data", {}).get("gpuTypes", [])
    with open("gpu_prices.json", "w") as f:
        json.dump(data, f, indent=2)
    print("✅ Saved gpu_prices.json with full pricing and location info")

except requests.exceptions.HTTPError as http_err:
    print(f"❌ HTTP error occurred: {http_err}")
    print(response.text)
except requests.exceptions.ConnectionError as conn_err:
    print(f"❌ Connection error occurred: {conn_err}")
except requests.exceptions.Timeout as timeout_err:
    print(f"❌ Timeout error occurred: {timeout_err}")
except requests.exceptions.RequestException as req_err:
    print(f"❌ An unexpected error occurred: {req_err}")
except Exception as e:
    print(f"❌ An error occurred: {e}")
