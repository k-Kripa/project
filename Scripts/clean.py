import pandas as pd
from pathlib import Path
import shutil

## Step 1. File and Folder path setup
# Locate project folders
folder= Path(__file__).resolve().parent.parent 
raw_data_folder = folder / "data" / "raw"
cleaned_data_folder = folder / "data" / "cleaned"

# Ensure directories exist
raw_data_folder.mkdir(parents=True, exist_ok=True)
cleaned_data_folder.mkdir(parents=True, exist_ok=True)

original_file = raw_data_folder / "realty_properties.csv"
duplicate_file = raw_data_folder / "realty_properties_cleaning.csv"

## Step 2 & 3 : Load,Select & Rename Columns
# 1. copy and load your dataset

shutil.copy2(original_file,duplicate_file)
df_1= pd.read_csv(duplicate_file)
print(f"Orginal shape:{df_1.shape}")

# 2: Select the 12 useful columns and rename 
columns_to_keep = [
    "property_id", "status", "list_date", "list_price",
    "price_reduced_amount", "location.address.city",
    "location.address.state", "location.address.postal_code",
    "description.beds", "description.baths", "description.sqft",
    "description.type"
]
df_1 = df_1[columns_to_keep]

# Save the selected columns to a new Csv file
output_file= folder/"realty_properties_selected.csv"
df_1.to_csv(output_file,index=False)
print("Selected dataset saved successfully")

# : Rename columns to simpler, cleaner names
df_1 = df_1.rename(columns={
    "property_id": "Property_id",
    "status": "Status",
    "list_date": "List_date",
    "list_price": "List_price",
    "price_reduced_amount": "Amount_reduced",
    "location.address.city": "City",
    "location.address.state": "State",
    "location.address.postal_code": "Postal_code",
    "description.beds": "Bedrooms",
    "description.baths": "Bathrooms",
    "description.sqft": "Property_sqft",
    "description.type": "Property_type"
})
print("Shape after selecting & renaming columns:", df_1.shape)
print(df_1.columns.tolist())

## Step 4 : Inital data inspection and data Handling

print(df_1.duplicated().sum())
print("Exact Duplicate rows :",df_1["Property_id"].duplicated().sum())
duplicate_ids=df_1[df_1["Property_id"].duplicated(keep=False)]
print(duplicate_ids)

#  counting how many non_null values a row has (completeness score)

df_1["data_completness"]=df_1.notnull().sum(axis=1) 

# calculating the average list price for each property 

# Rule 2: Price Alignment Check
# Calculate the average list price for each property type across the dataset
type_avg_prices = df_1.groupby("Property_type")["List_price"].transform("mean")

# Calculate how far this property's price is from the average of that property type
df_1["price_diff_from_avg"] = (df_1["List_price"] - type_avg_prices).abs()


# Favor single family over multi family if completeness and price check are equal
df_1["type_priority"]=df_1["Property_type"].apply(lambda x : 1 if x == "single_family" else 2)


# Sort strictly by your rules:
# 1. Property_id (groups duplicate rows together)
# 2. info_completeness DESCENDING (keeps full info, discards half/empty info)
# 3. price_diff_from_avg ASCENDING (keeps row closer to market price average)
# 4. type_priority ASCENDING (single_family over multi_family tie-breaker)
# 5. List_date DESCENDING (keeps the most recent listing date)

df_1 = df_1.sort_values(
    by=["Property_id", "data_completness", "price_diff_from_avg", "type_priority", "List_date"],
    ascending=[True, False, True, True, False])

# keeping the top-ranked record based on your rules
df_1=df_1.drop_duplicates(subset=["Property_id"],keep="first")
print(df_1.shape)

# remove helper columns use for sorting
df_1=df_1.drop(columns= ["data_completness", "price_diff_from_avg", "type_priority"])
print(df_1.shape)

## Step 5 :  Missing Vallue Handling 
#1. Land
df_1.loc[df_1["Property_type"]=="land"][["Bedrooms","Bathrooms"]]=df_1.loc[df_1["Property_type"]=="land",['Bedrooms',"Bathrooms"]].fillna(0)

## Step 6 : Drop residential properties missing essential data
df_1 = df_1.dropna(subset=["Bathrooms","Property_sqft"])

## Step 7: Standarize text casing and strip whitespace

# df_1["List_date"]=df_1["List_date"].astype(str).str.replace(r"-\s+","-",regex=True)
df_1["Property_type"]=df_1["Property_type"].str.strip().str.lower()
df_1["City"]=df_1["City"].str.strip().str.title()

# Step 8 : Remove unrealistic price outliers 
df_1=df_1[df_1["List_price"]>0]
df_1=df_1[df_1["Amount_reduced"]>0] 



# Step 9 : Data cleaning,prasing and Time Stripping
# Standarize list date to datetime formate
df_1["List_date"]=df_1["List_date"].astype(str).str.replace(r"-\s+","-",regex=True)
df_1["List_date"]=pd.to_datetime(df_1["List_date"],errors = "coerce").dt.strftime('%Y-%m-%d')

## Step 10: Engineer price_per_sqft column
 
df_1["Price_per_sqft"]=df_1["List_price"]/df_1["Property_sqft"]
df_1.loc[df_1["Property_type"]== "land", "Price_per_sqft"]=0
df_1["Price_per_sqft"]= df_1["Price_per_sqft"].round(2)

#Explicitly cast column data types
df_1["Bedrooms"]=df_1["Bedrooms"].astype(int)
df_1["Bathrooms"]=df_1["Bathrooms"].astype(float)
df_1["List_price"]=df_1["List_price"].astype(float)
df_1["Amount_reduced"]=df_1["Amount_reduced"].fillna(0).astype(float)
df_1["Property_type"]=df_1["Property_type"].astype(str)
df_1["City"]=df_1["City"].astype(str)

## Save final Dataset
output_file= cleaned_data_folder/"properties_cleaned.csv"
df_1.to_csv(output_file,index=False)
#
print(output_file)
print(df_1.head())