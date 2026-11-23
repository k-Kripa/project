# Real Estate Business Analytics (ZIP 90004, Los Angeles)

End-to-end analytics project: pull listings from the Realty API, clean them with pandas,
load them into PostgreSQL, analyse with SQL, and explore in a Jupyter notebook.

## Data
- Source: Realty-in-US API (RapidAPI), listings for sale in ZIP code **90004** only.
- One snapshot (see the `pull_date` column when you re-run `extract.py`).
- Raw: 145 rows. Cleaned: 119 rows incl. 8 land listings (with 25 extreme listings flagged via 'is_outlier').

## Project structure
- `scripts/extract.py` - download raw data (needs `RAPIDAPI_KEY` in `.env`)
- `scripts/clean.py` - clean data, flag outliers (`is_outlier`)
- `scripts/load_to_db.py` - load the cleaned CSV into PostgreSQL
- `scripts/analysis.ipynb` - notebook analysis with charts
- `sql/queries.sql` - 10 analytical queries
- `data/raw`, `data/cleaned` - raw and cleaned CSV snapshots
- `powerbi/` - Power BI dashboard file (`.pbix`)
- `screenshot/` - dashboard previews (all listings and non-outliers)

## How to run
1. `pip install -r requirements.txt`
2. Create a `.env` file in the project root with your own API and database credentials (never     commit `.env`).
3. `python scripts/extract.py`
4. `python scripts/clean.py`
5. `python scripts/load_to_db.py`
6. Run `sql/queries.sql`, then open `scripts/analysis.ipynb`.

## Key findings
- Across the 119 cleaned listings in ZIP code 90004 (from 145 raw listings), the overall median list price is $1.65M compared to an average of $2.55M ($2,547,974), showing how high-priced properties pull the mean upward.

- Single-family homes (48 listings, 40.3%) and multi-family properties (45 listings, 37.8%) make up nearly four-fifths of the market, followed by condos (17 listings, 14.3%), land (8 listings, 
6.7%), and townhomes (1 listing, 0.8%).

- By median list price across all 119 listings, land ($1,975,000) and multi-family properties ($1,925,000) rank highest, followed by single-family homes ($1,724,500), townhomes ($1,048,000), and condos ($735,000).

- Most listings fall in the High-end ($1.5M–$3.5M: 45 listings, 37.8%) and Mid-range ($750K–$1.5M: 42 listings, 35.3%) tiers, followed by Ultra-luxury ($5M+: 13 listings, 10.9%), Entry (under $750K: 10 listings, 8.4%), and Luxury ($3.5M–$5M: 9 listings, 7.6%).

- Overall, 29.41% of listings (35 of 119) had a price reduction, led by condos, while 93.28% (111 listings) were listed in 2026 versus 6.72% (8 listings) carried over from 2025.

- Exactly 25 of the 119 cleaned listings are flagged as outliers (`is_outlier` = True ,for over 10 bedrooms or list prices above $10M); filtering to non-outliers (`is_outlier`= False , 94 listings) lowers the average list price from $2.55M to $1.89M ($1,893,988) and the median from $1.65M to $1.47M.

## Dashboard previews

- `screenshot/01.market_overview_all_listings.png` – Executive Market Overview (all 119 listings)
- `screenshot/02.market_overview_no_outliers.png` – Executive Market Overview (`is_outlier' = False`, 94 listings)
- `screenshot/03.price_segmentation_all_listings.png` – Price Segmentation (all 119 listings)
- `screenshot/04.price_segmentation_no_outliers.png` – Price Segmentation (`is_outlier = False`, 94 listings)

## Limitations

- One ZIP code and one day, so results do not describe all of Los Angeles.
- Multi-family buildings and luxury homes pull averages up; compare medians.

## Technologies

Python (requests, pandas, python-dotenv, SQLAlchemy), PostgreSQL, Power BI, Git.