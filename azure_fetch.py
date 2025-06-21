import requests
import json

def fetch_azure_gpu_prices(region="eastus"):
    prices = []
    url = f"https://prices.azure.com/api/retail/prices?$filter=serviceFamily eq 'Compute' and armRegionName eq '{region}'"

    while url:
        print(f"Fetching: {url}")
        res = requests.get(url)
        data = res.json()

        for item in data.get("Items", []):
            if "GPU" in item.get("productName", "") or "GPU" in item.get("meterName", ""):
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
