import os
import time
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
frames=[]
for page in range (1,11):
    querystring={"query":"Phone","page":str(page),"country":"US","sort_by":"RELEVANCE","product_condition":"ALL"}
response = requests.get(url, headers=headers, params=querystring,timeout=30)
if response.status_code !=200:
  print(f"page{page} failed -> {response.status_code}")
  continue
products= response.json()["data"]["products"]
df_page= pd.json_normalize(products)
df_page["search_page"]=page
frames.append(df_page)
print(f"page{page}:{len(df_page)} rows")
time.sleep(1)
df= pd.concat(frames,ignore_index=True)
os.makedirs("data/raw",exist_ok=True)
df.to_csv("data/raw/amazon_phones_raw.csv",index=False)
print(df.shape)