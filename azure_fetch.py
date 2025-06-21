import requests
import json

# רשימת GPUים שאנחנו רוצים לכלול – רק דגמים אמיתיים
ALLOWED_GPU_MODELS = [
    "B200", "H200", "H100", "A100", "RTX 3090", "RTX 4090", "RTX 5090",
    "RTX 2000", "RTX 4000", "RTX 6000", "RTX A4000", "RTX A4500", "RTX A5000",
    "RTX A6000", "RTX PRO 6000", "L4", "L40", "L40S", "A40"
]

# רשימת מילים שאם הן מופיעות בשמות – אנחנו נדחה (לא GPU)
EXCLUDE_IF_CONTAINS = [
    "D", "E", "F", "G", "L", "Ls", "Lsv3", "L48", "L64", "Ebsv5", "Dadsv5",
    "M", "B", "H", "Dv4", "Ev4", "FX", "FX-series"
]

# אזורים רלוונטיים
AZURE_REGIONS = [
    "eastus", "westus", "westus2", "centralus", "northeurope", "westeurope",
    "eastasia", "southeastasia", "japaneast", "japanwest", "australiaeast",
    "australiasoutheast", "canadacentral", "uksouth", "francecentral",
    "swedencentral", "germanywestcentral", "brazilsouth", "southafricanorth"
]

def is_gpu_item(sku, product):
    combined = f"{sku} {product}".upper()

    # סינון חיובי – רק אם יש התאמה לאחד הדגמים
    if not any(model.upper() in combined for model in ALLOWED_GPU_MODELS):
        return False

    # סינון שלילי – אם יש התאמה לאחד מהמופעים הלא רצויים
    if any(excl.upper() in combined for excl in EXCLUDE_IF_CONTAINS):
        return False

    return True

def fetch_gpu_prices_for_region(region):
    prices = []
    url = f"https://prices.azure.com/api/retail/prices?$filter=serviceFamily eq 'Compute' and armRegionName eq '{region}'"

    while url:
        print(f"📥 Fetching region: {region}")
        res = requests.get(url)
        data = res.json()

        for item in data.get("Items", []):
            sku = item.get("skuName", "")
            product = item.get("productName", "")
            if is_gpu_item(sku, product):
                prices.append({
                    "region": item["armRegionName"],
                    "skuName": sku,
                    "productName": product,
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
