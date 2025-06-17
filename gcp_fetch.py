# gcp_fetch.py
import os
import json
import requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request

# טען את מפתח ה־Service Account מה-ENV
SA_JSON = os.environ["GCP_SA_KEY"]
info = json.loads(SA_JSON)
creds = service_account.Credentials.from_service_account_info(info)
scoped = creds.with_scopes(["https://www.googleapis.com/auth/cloud-billing"])

# רענן את הטוקן
scoped.refresh(Request())

# כתובת API של GPU pricing
url = "https://cloudbilling.googleapis.com/v1/services/6F81-5844-456A/skus"
headers = {"Authorization": f"Bearer {scoped.token}"}

def fetch_gpu_skus():
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
            desc = sku.get("description", "")
            if "GPU" in desc and sku.get("pricingInfo"):
                # נירמול nanos למחיר בדולרים לשעה
                price_info = sku["pricingInfo"][0]
                tier = price_info["pricingExpression"]["tieredRates"][0]
                nanos = tier["unitPrice"].get("nanos", 0)
                units = int(tier["unitPrice"].get("units", 0))
                secure_price = units + nanos / 1e9

                skus.append({
                    "skuId": sku["skuId"],
                    "description": desc,
                    "securePrice": round(secure_price, 4)
                })

        page_token = data.get("nextPageToken", "")
        if not page_token:
            break
    return skus

if __name__ == "__main__":
    skus = fetch_gpu_skus()
    with open("gcp_gpu_prices_normalized.json", "w") as f:
        json.dump(skus, f, indent=2)
    print("✅ gcp_gpu_prices_normalized.json saved")
