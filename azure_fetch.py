import requests
import json

# רשימת דגמים שאתה רוצה לראות בתוצאה הסופית
ALLOWED_GPU_MODELS = [
    "B200", "H200", "H100", "A100", "RTX 3090", "RTX 4090", "RTX 5090",
    "RTX 2000", "RTX 4000", "RTX 6000", "RTX A4000", "RTX A4500", "RTX A5000",
    "RTX A6000", "RTX PRO 6000", "L40", "L40S", "A40"
]

# רשימת אזורים רלוונטיים ב-Azure
AZURE_REGIONS = [
    "eastus", "westus", "westus2", "centralus", "northeurope", "westeurope",
    "eastasia", "southeastasia", "japaneast", "japanwest", "australiaeast",
    "australiasoutheast", "canadacentral", "uksouth", "francecentral",
    "swedencentral", "germanywestcentral", "brazilsouth", "southafricanorth"
]

def fetch_gpu_prices_for_region(region):
    prices = []
    url = f"https://prices.azure.com/api/retail/prices?$filter=serviceFamily eq 'Compute' and armRegionName eq '{region}'"

    while url:
        print(f"📥 Fetching region: {region}")
        res = requests.get(url)
        data = res.json()

        for item in data.get("Items", []):
            sku = item.get("skuName", "").upper()
            product = item.get("productName", "").upper()
            combined = f"{sku} {product}"

            if any(model.upper() in combined for model in ALLOWED_GPU_MODELS):
                prices.append({
                    "region": item["armRegionName"],
                    "skuName": item["skuName"],
                    "productName": item["productName"],
                    "pricePerHour": item["retailPrice"],
                    "currency": item["currencyCode"]
                })

        url = data.get("NextPageLink")

    return prices

def fetch_all_azure_gpu_prices():
    all_prices = []
    for region in AZURE_REGIONS:
        all_prices.extend(fetch_gpu_prices_for_region(region))

    with open("azure_gpu_prices.json", "w") as f:
        json.dump(all_prices, f, indent=2)

    print(f"✅ Saved {len(all_prices)} GPU price entries to azure_gpu_prices.json")

if __name__ == "__main__":
    fetch_all_azure_gpu_prices()
