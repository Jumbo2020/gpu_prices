import requests
import json

# הגדר את ה-API Key שלך
API_KEY = "rpa_EGTLJ7QBY4JW5T087XQZ25IDFKZ21KFBPMLMTX2Lic6jwh"

# כתובת ה-API של RunPod
url = "https://api.runpod.io/graphql"

# headers לבקשה
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# שאילתת GraphQL שמביאה מחירים + מיקומים
query = """
query {
  gpuTypes(input: { secureCloud: true }) {
    displayName
    secureCloud
    securePrice
    threeMonthPrice
    sixMonthPrice
    nodeGroupDatacenters {
      id
      name
      region
    }
  }
}
"""

# שליחת הבקשה
response = requests.post(url, headers=headers, json={"query": query})
response.raise_for_status()

# עיבוד התוצאה
data = response.json()["data"]["gpuTypes"]

# שמירה כ-json
with open("gpu_prices.json", "w") as f:
    json.dump(data, f, indent=2)

print("✅ gpu_prices.json updated successfully.")
