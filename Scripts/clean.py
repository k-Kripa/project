"""Step 2 - Clean the raw listings and save data/cleaned/properties_cleaned.csv."""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw" / "realty_properties.csv"
OUT = ROOT / "data" / "cleaned" / "properties_cleaned.csv"

KEEP = {
    "property_id": "property_id",
    "status": "status",
    "list_date": "list_date",
    "list_price": "list_price",
    "price_reduced_amount": "amount_reduced",
    "location.address.city": "city",
    "location.address.state": "state",
    "location.address.postal_code": "postal_code",
    "description.beds": "bedrooms",
    "description.baths": "bathrooms",
    "description.sqft": "property_sqft",
    "description.type": "property_type",
}


def load(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df = df[list(KEEP)].rename(columns=KEEP)      # select and rename in one step
    print("Loaded:", df.shape)
    return df


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Keep ONE row per property_id: the most complete one, then the newest."""
    before = len(df)
    df = df.assign(_completeness=df.notnull().sum(axis=1))
    df = df.sort_values(["property_id", "_completeness", "list_date"],
                        ascending=[True, False, False])
    df = df.drop_duplicates("property_id", keep="first").drop(columns="_completeness")
    print(f"Duplicate property_id rows removed: {before - len(df)}")
    return df


def handle_missing(df: pd.DataFrame) -> pd.DataFrame:
    df["amount_reduced"] = df["amount_reduced"].fillna(0)
    is_land = df["property_type"].str.strip().str.lower() == "land"
    df.loc[is_land, ["bedrooms", "bathrooms", "property_sqft"]] = (
        df.loc[is_land, ["bedrooms", "bathrooms", "property_sqft"]].fillna(0)
    )

    before = len(df)
    df = df.dropna(subset=["bedrooms", "bathrooms", "property_sqft"])
    print(f"Rows dropped for missing beds/baths/sqft: {before - len(df)}")
    return df


def standardise(df: pd.DataFrame) -> pd.DataFrame:
    df["property_type"] = df["property_type"].str.strip().str.lower()
    df["city"] = df["city"].str.strip().str.title()
    df["list_date"] = pd.to_datetime(df["list_date"], errors="coerce").dt.strftime("%Y-%m-%d")
    return df


def remove_bad_values(df: pd.DataFrame) -> pd.DataFrame:
    before = len(df)
    df = df[df["list_price"] > 0]
    df = df[(df["amount_reduced"] >= 0) & (df["amount_reduced"] < df["list_price"])]
    df = df.assign(is_outlier=(df["bedrooms"] > 10) | (df["list_price"] > 10_000_000))
    print(f"Rows removed for bad prices: {before - len(df)}; flagged outliers: {int(df['is_outlier'].sum())}")
    return df


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    has_sqft = df["property_sqft"] > 0
    df["price_per_sqft"] = 0.0
    df.loc[has_sqft, "price_per_sqft"] = (df["list_price"] / df["property_sqft"]).round(2)
    df["bedrooms"] = df["bedrooms"].astype(int)
    df["bathrooms"] = df["bathrooms"].astype(float)
    return df


def main() -> None:
    df = load(RAW)
    df = remove_duplicates(df)
    df = handle_missing(df)
    df = standardise(df)
    df = remove_bad_values(df)
    df = add_features(df)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT, index=False)
    print("Saved", OUT, df.shape)
    print(df["property_type"].value_counts())


if __name__ == "__main__":
    main()