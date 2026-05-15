import argparse
import pandas as pd

from scraper.steam_scraper import scrape_steam_games
from analysis.analysis import (
    clean_dataframe,
    process_data,
    run_business_analysis,
    save_cleaned_csv
)
from analysis.visualization import (
    generate_visualizations
)
from database.mongodb_connection import (
    upsert_games
)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Steam Games Market Analysis Pipeline"
    )

    parser.add_argument(
        "--refresh",
        action="store_true",
        help=(
            "Force a fresh scrape and update MongoDB Atlas. "
            "Use this when Steam data must be refreshed."
        )
    )

    parser.add_argument(
        "--export-csv",
        action="store_true",
        help="Export cleaned dataset to output/csv as an optional backup."
    )

    parser.add_argument(
        "--max-pages",
        type=int,
        default=80,
        help="Maximum Steam search pages to scrape (50 games per page)."
    )

    return parser.parse_args()


def refresh_data(max_pages, export_csv=False):
    print("\nSTEP 1: Steam Web Scraping")

    raw_games = scrape_steam_games(page_count=max_pages)

    if not raw_games:
        print("No games were scraped. Aborting refresh.")
        return None

    print("\nSTEP 2: Cleaning Scraped Data")

    cleaned_df = clean_dataframe(pd.DataFrame(raw_games))
    cleaned_df = cleaned_df.drop_duplicates(subset=["title"]).reset_index(drop=True)

    print("\nSTEP 3: MongoDB Upsert")

    upsert_games(cleaned_df.to_dict(orient="records"))

    if export_csv:
        save_cleaned_csv(cleaned_df)

    return cleaned_df


def main():
    args = parse_arguments()

    print("=" * 60)
    print("STEAM GAMES MARKET ANALYSIS PROJECT")
    print("=" * 60)

    if args.refresh:
        cleaned_df = refresh_data(
            max_pages=args.max_pages,
            export_csv=args.export_csv
        )

        if cleaned_df is None or cleaned_df.empty:
            return
    else:
        print("\nSTEP 1: Load Data From MongoDB Atlas")

        cleaned_df = process_data()

        if cleaned_df is None or cleaned_df.empty:
            print(
                "\nNo data was found in MongoDB Atlas or backup CSV."
            )
            print(
                "Run the script with --refresh to scrape and populate Atlas."
            )
            return

    print("\nSTEP 4: Business Analytics")

    run_business_analysis(cleaned_df)

    print("\nSTEP 5: Data Visualization")

    generate_visualizations(cleaned_df)

    print("\nPROJECT PIPELINE COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()