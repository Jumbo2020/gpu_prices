import requests
import json

# רשימת SKUים שידוע שהם כוללים GPU
KNOWN_GPU_SKUS = [
    "NC", "NCv2", "NCv3", "NCasT4_v3", "ND", "NDv2", "NDm_A100_v4",
    "NV", "NVv3", "NVv4", "Standard_ND40rs_v2", "ND96asr_v4"
]

def fetch_azure_gpu_prices(region="eastus"):
    prices = []
    url = f"https://prices.azure.com/api/retail/prices?$filter=serviceFamily eq 'Compute' and armRegionName eq '{region}'"

    while url:
        print(f"Fetching: {url}")
        res = requests.get(url)
        data = res.json()

        for item in data.get("Items", []):
            sku = item.get("skuName", "").lower()
            if any(gpu.lower() in sku for gpu in KNOWN_GPU_SKUS):
                prices.append({
                    "region": item["armRegionName"],
                    "skuName": item["skuName"],
                    "productName": item["productName"],
                    "pricePerHour": item["retailPrice"],
                    "currency": item["currencyCode"]
                })

        url = data.get("NextPageLink")

    with open("azure_gpu_prices.json", "w") as f:
        json.dump(prices, f, indent=2)

    print(f"✅ Saved {len(prices)} GPU price entries to azure_gpu_prices.json")

if __name__ == "__main__":
    fetch_azure_gpu_prices()
