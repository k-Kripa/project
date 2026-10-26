import os
import pandas as pd
import requests
from dotenv import dotenv_values
config= dotenv_values(".env")

url = "https://real-time-amazon-data.p.rapidapi.com/search"

querystring = {"query":"Phone","page":"1","country":"US","sort_by":"RELEVANCE","product_condition":"ALL","is_prime":"false","deals_and_discounts":"NONE"}

headers = {
	"x-rapidapi-key":config["RAPIDAPI_KEY"],
	"x-rapidapi-host": "real-time-amazon-data.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)
print(response.status_code)

data = response.json()
print(data.keys())
print(data["data"].keys())

df = pd.json_normalize(data["data"]["products"])
os.makedirs("data/raw", exist_ok=True)
df.to_csv("data/raw/amazon_phone_page1.csv", index=False)
print(df.head())
