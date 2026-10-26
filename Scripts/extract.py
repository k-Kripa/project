import os
import time
import pandas as pd
import requests
from dotenv import dotenv_values
config= dotenv_values(".env")
import requests

url = "https://realty-in-us.p.rapidapi.com/properties/v3/list"

payload = {
	"limit": 200,
	"offset": 0,
	"postal_code": "90004",
	"status": ["for_sale", "ready_to_build"],
	"sort": {
		"direction": "desc",
		"field": "list_date"
	}
}
headers = {
	"x-rapidapi-key": config["RAPIDAPI_KEY"],
	"x-rapidapi-host": "realty-in-us.p.rapidapi.com",
	"Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print(response.json())

data= response.json()
print(data["data"].keys())
print(data["data"]["home_search"].keys())

df= pd.json_normalize(data["data"]["home_search"]["results"])
os.makedirs("data/raw",exist_ok=True)
df.to_csv("data/raw/realty_properties.csv",index=False)
print(f"Successfully saved {len(df)}properties!")
print(df.shape)
print(df.columns.tolist())