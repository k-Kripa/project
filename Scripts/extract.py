"""Step 1 - Download listings from the Realty API and save the raw CSV."""
import os
import sys
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv

ROOT= Path(__file__).resolve().parent.parent
load_dotenv (ROOT/".env")                         # reads RAPIDAPI_KEY FROM .ENV

API_KEY=os.getenv("RAPIDAPI_KEY")
if not API_KEY:
    sys.exit("RAPIDAPI_KEY is missing.Add it to your .env file.")

url = "https://realty-in-us.p.rapidapi.com/properties/v3/list"
HEADERS = {
	"x-rapidapi-key": API_KEY,
	"x-rapidapi-host": "realty-in-us.p.rapidapi.com",
	"Content-Type": "application/json"
}
PAGE_SIZE = 200
POSTAL_CODE= "90004"

def fetch_page(offset:int)-> list :
    payload={
        "limit":PAGE_SIZE,
        "offset": offset,
        "postal_code": POSTAL_CODE,
        "status":["for_sale","ready_to_build"],
        "sort":{"direction":"desc","field":"list_date"},
	}
    response=requests.post(url,json=payload,headers=HEADERS,timeout=30)
    response.raise_for_status()
    body=response.json()
    return body["data"]["home_search"]["results"]


def main()-> None:
    rows,offset=[],0
    while True:
        page=fetch_page(offset)
        rows.extend(page)
        if len (page)< PAGE_SIZE :
            break
        offset += PAGE_SIZE
    df=pd.json_normalize(rows)
    df=df.drop(columns=[c for c in df.columns if "street_view" in c])
    df["pull_date"]=pd.Timestamp.today().strftime("%Y-%m-%d")
    
    out= ROOT/"data"/"raw"/"realty_properties.csv"
    out.parent.mkdir(parents=True,exist_ok=True)
    df.to_csv(out,index=False)
    print(F"Saved {len(df)} listings to {out}")

if __name__=="__main__":
    main()