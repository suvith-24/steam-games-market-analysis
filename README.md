# Steam Games Market Analysis using Web Scraping and MongoDB

A reproducible Python data pipeline that scrapes Steam game listings, cleans the data, stores it in MongoDB Atlas, and produces analytics and visualizations.

---

# Project Summary

This repository implements a cloud-based data flow where MongoDB Atlas serves as the primary datasource. The code is organized so scraping is optional, data cleaning is centralized, and analytics/visualizations read directly from Atlas.

---

# Project Flow

1. `scraper/steam_scraper.py` requests Steam search pages and returns raw game records.
2. `analysis/analysis.py` cleans raw records, transforms prices, discounts, platforms, and classifies games.
3. `database/mongodb_connection.py` connects to MongoDB Atlas, creates indexes, and upserts cleaned data.
4. `analysis/visualization.py` loads cleaned data directly from MongoDB and generates charts.
5. `main.py` controls the pipeline, supports optional refresh, and manages CSV backups.

---

# Features

- Scrape Steam only when `--refresh` is used.
- Prevent duplicate records in MongoDB Atlas using title-based unique upsert.
- Support optional backup CSV export.
- Load analytics and charts directly from MongoDB Atlas.
- Maintain modular structure for easy reuse and extension.

---

# Tech Stack

- Python
- requests
- BeautifulSoup
- pandas
- pymongo
- MongoDB Atlas
- matplotlib
- seaborn
- python-dotenv

---

# Repository Structure

```text
steam-games-market-analysis/
│
├── scraper/
│   └── steam_scraper.py          # Steam scraping logic
│
├── database/
│   └── mongodb_connection.py     # Atlas connection, upsert, and data loading
│
├── analysis/
│   ├── analysis.py               # Data cleaning and analytics
│   └── visualization.py          # Chart generation from Atlas data
│
├── output/
│   ├── charts/                   # Generated chart images
│   └── csv/                      # Optional CSV backup exports
│
├── main.py                       # Main pipeline runner and CLI interface
├── requirements.txt              # Python dependencies
├── README.md                     # Project documentation
├── prompts_used.txt              # Prompt history / notes
├── .env                          # Local environment variables (private)
├── .env.example                  # Example environment template
├── .gitignore                    # Ignore rules for Git
```

---

# Prerequisites

- Python 3.10 or later
- MongoDB Atlas account
- Git installed for repo version control

---

# Setup Instructions

## 1. Clone the Repository

```powershell
cd "c:\Users\Suvith Shetty\OneDrive\Desktop\SRH\SEMESTER 2\Data Management 2"

git clone <your-github-repo-url>

cd steam-games-market-analysis
```

---

## 2. Create and Activate Virtual Environment

If the `venv` folder already exists:

```powershell
.\venv\Scripts\Activate.ps1
```

Otherwise:

```powershell
python -m venv venv

.\venv\Scripts\Activate.ps1

python -m pip install -r requirements.txt
```

---

# MongoDB Atlas Setup

## 1. Create Atlas Cluster

1. Create a MongoDB Atlas account.
2. Create a new cluster.
3. Free tier is sufficient.

---

## 2. Configure Network Access

Add your current IP address in:

```text
Security → Network Access
```

You can temporarily allow:

```text
0.0.0.0/0
```

for development.

---

## 3. Create Database User

Create a MongoDB user with:

```text
readWrite
```

permissions.

---

## 4. Configure Environment Variables

Create:

```text
.env
```

inside the project root.

Example:

```env
MONGO_URI=mongodb+srv://<username>:<password>@<cluster-url>/steam_games_db?retryWrites=true&w=majority
```

---

# MongoDB Atlas Details

The project uses:

```text
Database:
steam_games_db
```

```text
Collection:
steam_games
```

Features:
- Unique index on `title`
- Bulk upsert operations
- MongoDB Atlas as primary datasource
- CSV only used as backup fallback

---

# Running the Project

## Run Analytics From MongoDB Atlas

```powershell
.\venv\Scripts\python.exe main.py
```

This:
- loads data directly from MongoDB Atlas
- runs analytics
- generates visualizations

No scraping occurs.

---

## Refresh Steam Data and Update Atlas

```powershell
.\venv\Scripts\python.exe main.py --refresh --export-csv
```

This:
- scrapes Steam again
- cleans data
- updates MongoDB Atlas
- exports optional CSV backup

---

## Quick Test Run

```powershell
.\venv\Scripts\python.exe main.py --refresh --max-pages 1 --export-csv
```

Useful for testing without scraping thousands of records.

---

# CLI Options

| Option | Description |
|---|---|
| `--refresh` | Scrape Steam again and update Atlas |
| `--export-csv` | Save cleaned backup CSV |
| `--max-pages <n>` | Limit Steam pages scraped |

---

# Expected Outputs

## MongoDB Atlas

```text
steam_games_db.steam_games
```

Stores:
- cleaned Steam records
- prices
- discounts
- platforms
- classifications

---

## CSV Backup

```text
output/csv/steam_games_cleaned.csv
```

Optional fallback dataset.

---

## Charts

```text
output/charts/
```

Contains generated visualizations.

---

# Troubleshooting

## MongoDB Connection Errors

Check:
- `.env` exists
- `MONGO_URI` is correct
- Atlas IP access is enabled
- database user has permissions

---

## Empty Charts or Missing Data

Run:

```powershell
python main.py --refresh
```

to populate Atlas.

---

## Python Package Errors

Reinstall dependencies:

```powershell
python -m pip install -r requirements.txt
```

---

# GitHub Push Instructions

## First Push

```powershell
git init

git add .

git commit -m "Initial commit"

git branch -M main

git remote add origin <your-github-url>

git push -u origin main
```

---

## Future Pushes

```powershell
git add .

git commit -m "Updated project"

git push
```

---

# Important Notes

- `.env` should NEVER be pushed to GitHub.
- MongoDB Atlas is the main datasource.
- CSV is only a fallback backup.
- Scraping occurs only with `--refresh`.

---

# File Responsibilities

| File | Responsibility |
|---|---|
| `main.py` | Pipeline runner and CLI |
| `scraper/steam_scraper.py` | Steam scraping |
| `analysis/analysis.py` | Cleaning and analytics |
| `database/mongodb_connection.py` | Atlas connection and upserts |
| `analysis/visualization.py` | Visualization generation |

---

# Example Workflow

## First Time

```powershell
python main.py --refresh --export-csv
```

This:
1. Scrapes Steam
2. Cleans data
3. Uploads to MongoDB Atlas
4. Exports backup CSV

---

## Daily Analytics Run

```powershell
python main.py
```

This:
1. Loads data from Atlas
2. Runs analytics
3. Generates charts

No scraping required.

---

# Author

Suvith Shetty

Data Engineering / Data Analytics / AI & ML