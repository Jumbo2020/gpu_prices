import requests, json

API_KEY = "Bearer rpa_…"
URL = "https://api.runpod.io/graphql"
query = """{ gpuTypes { id displayName memoryInGb maxGpuCount secureCloud communityCloud securePrice communityPrice communitySpotPrice secureSpotPrice clusterPrice } }"""
r = requests.post(URL, headers={"Authorization":API_KEY,"Content-Type":"application/json"}, json={"query":query})
print(r.status_code, r.text[:300])
if r.status_code==200:
    data = r.json().get("data",{}).get("gpuTypes",[])
    with open("gpu_prices.json","w") as f: json.dump(data,f,indent=2)
    print("🟢 Saved gpu_prices.json")
else:
    print("❌",r.text)
