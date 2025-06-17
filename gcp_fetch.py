# gcp_fetch.py
import os, json, google.auth, requests
from google.oauth2 import service_account

# env var with full JSON SA key
SA_JSON = os.environ["GCP_SA_KEY"]
info = json.loads(SA_JSON)
creds = service_account.Credentials.from_service_account_info(info)
scoped = creds.with_scopes(["https://www.googleapis.com/auth/cloud-billing"])

def fetch_gpu_skus():
    url = "https://cloudbilling.googleapis.com/v1/services/6F81-5844-456A/skus"
    headers = {"Authorization": "Bearer " + scoped.token}
    skus = []
    page_token = ""
    while True:
        params = {"pageSize": 500, "pageToken": page_token} if page_token else {"pageSize":500}
        resp = requests.get(url, headers=headers, params=params)
        resp.raise_for_status()
        data = resp.json()
        for s in data.get("skus", []):
            if "GPU" in s.get("description", ""):
                skus.append({
                    "skuId": s["skuId"],
                    "description": s["description"],
                    "pricingInfo": s.get("pricingInfo", [])
                })
        page_token = data.get("nextPageToken", "")
        if not page_token:
            break
    return skus

if __name__ == "__main__":
    skus = fetch_gpu_skus()
    with open("gcp_gpu_prices.json", "w") as f:
        json.dump(skus, f, indent=2)
    print("✅ gcp_gpu_prices.json saved")
