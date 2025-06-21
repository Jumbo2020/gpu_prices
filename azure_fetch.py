
import requests
import json
import os

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
    """
    Fetches GPU prices for a specific Azure region from the Azure Retail Prices API.
    """
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
            sku = item.get("skuName", "").upper()
            product = item.get("productName", "").upper()
            combined = f"{sku} {product}"

            if any(model.upper() in combined for model in ALLOWED_GPU_MODELS):
                prices.append({
                    "region": item["armRegionName"],
                    "skuName": item["skuName"],
                    "productName": item["productName"],
                    "pricePerHour": item["retailPrice"],
                    "currency": item["currencyCode"],
                    "unitOfMeasure": item.get("unitOfMeasure", "")
                })

        url = data.get("NextPageLink")

    return prices

def fetch_all_azure_gpu_prices(output_filename="azure_gpu_prices.json"):
    """
    Fetches all GPU prices across specified Azure regions and saves them to a JSON file.
    """
    all_prices = []
    for region in AZURE_REGIONS:
        all_prices.extend(fetch_gpu_prices_for_region(region))

    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(all_prices, f, indent=2, ensure_ascii=False)

    print(f"✅ Saved {len(all_prices)} GPU price entries to {output_filename}")
    return output_filename

def filter_gpu_prices(input_file="azure_gpu_prices.json", output_file="filtered_azure_gpu_prices.json"):
    """
    Filters GPU prices based on specified criteria:
    - Removes entries with "Low Priority" or "Spot" in skuName.
    - Keeps only prices between 0.1 and 200 USD/hour.
    """
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            all_prices = json.load(f)
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{input_file}'. Check file format.")
        return

    filtered_prices = []
    initial_count = len(all_prices)
    for item in all_prices:
        sku_name = item.get("skuName", "").lower()
        price_per_hour = item.get("pricePerHour")

        if any(term in sku_name.replace(" ", "") for term in ["lowpriority", "spot"]):
            continue

        try:
            price = float(price_per_hour)
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
    initial_data_file = fetch_all_azure_gpu_prices()
    if initial_data_file and os.path.exists(initial_data_file):
        filter_gpu_prices(input_file=initial_data_file)
    else:
        print("Skipping filtering as initial data file was not created or found.")
