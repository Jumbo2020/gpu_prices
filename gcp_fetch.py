# gcp_fetch.py
import os, json, requests
from google.oauth2 import service_account

# Load credentials from env var
SA_JSON = os.environ["GCP_SA_KEY"]
info = json.loads(SA_JSON)
creds = service_account.Credentials.from_service_account_info(info)
scoped = creds.with_scopes(["https://www.googleapis.com/auth/cloud-billing"])
scoped.refresh(requests.Request())

def fetch_gpu_skus():
    url = "https://cloudbilling.googleapis.com/v1/services/6F81-5844-456A/skus"
    headers = {"Authorization": "Bearer " + scoped.token}
    skus = []
    page_token = ""

    while True:
        params = {"pageSize": 500}
        if page_token:
            params["pageToken"] = page_token

        resp = requests.get(url, headers=headers, params=params)
        resp.raise_for_status()
        data = resp.json()

        for sku in data.get("skus", []):
            if "GPU" in sku.get("description", ""):
                pricing_info = sku.get("pricingInfo", [])
                if pricing_info:
                    tier = pricing_info[0]["pricingExpression"]["tieredRates"][0]
                    nanos = tier["unitPrice"].get("nanos", 0)
                    units = int(tier["unitPrice"].get("units", 0))
                    hourly_price = units + (nanos / 1_000_000_000)

                    skus.append({
                        "displayName": sku["description"],
                        "secureCloud": True,
                        "securePrice": round(hourly_price, 4),
                        "nodeGroupDatacenters": []
                    })

        page_token = data.get("nextPageToken", "")
        if not page_token:
            break

    return skus

if __name__ == "__main__":
    gpu_data = fetch_gpu_skus()
    with open("gcp_gpu_prices_normalized.json", "w") as f:
        json.dump(gpu_data, f, indent=2)
    print("✅ gcp_gpu_prices_normalized.json saved")
