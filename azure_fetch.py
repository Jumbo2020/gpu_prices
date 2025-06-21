
import requests
import json

ALLOWED_GPU_MODELS = [
    "B200", "H200", "H100", "A100", "RTX 3090", "RTX 4090", "RTX 5090",
    "RTX 2000", "RTX 4000", "RTX 6000", "RTX A4000", "RTX A4500", "RTX A5000",
    "RTX A6000", "RTX PRO 6000", "L40", "L40S", "A40"
]

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
        try:
            res = requests.get(url)
            res.raise_for_status()
            data = res.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for {region}: {e}")
            break
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON for {region}: {e}")
            break

        for item in data.get("Items", []):
            prices.append({
                "region": item.get("armRegionName", ""),
                "skuName": item.get("skuName", ""),
                "productName": item.get("productName", ""),
                "pricePerHour": item.get("retailPrice"),
                "currency": item.get("currencyCode", ""),
                "unitOfMeasure": item.get("unitOfMeasure", "")
            })

        url = data.get("NextPageLink")

    return prices

def fetch_all_azure_gpu_prices():
    all_prices = []
    for region in AZURE_REGIONS:
        all_prices.extend(fetch_gpu_prices_for_region(region))
    return all_prices

def filter_gpu_prices(all_prices, output_file="filtered_azure_gpu_prices.json"):
    filtered_prices = []
    initial_count = len(all_prices)

    for item in all_prices:
        sku_name = item.get("skuName", "").lower()
        product_name = item.get("productName", "").lower()
        combined = f"{sku_name} {product_name}"

        if not any(model.lower() in combined for model in ALLOWED_GPU_MODELS):
            continue

        if any(term in sku_name.replace(" ", "") for term in ["lowpriority", "spot"]):
            continue

        try:
            price = float(item.get("pricePerHour"))
            if price < 0.1 or price > 200:
                continue
        except (ValueError, TypeError):
            continue

        filtered_prices.append(item)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(filtered_prices, f, indent=2, ensure_ascii=False)

    print(f"✅ Filtered {len(filtered_prices)} GPU price entries saved to {output_file}")
    print(f"Removed {initial_count - len(filtered_prices)} entries during filtering.")

if __name__ == "__main__":
    all_prices = fetch_all_azure_gpu_prices()
    filter_gpu_prices(all_prices)
