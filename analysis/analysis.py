import ast
import os
import re
import pandas as pd
from database.mongodb_connection import (
    export_to_csv,
    load_data_from_db
)


def clean_price(price_text):
    """Convert Steam price text into numeric values."""

    if not price_text:
        return 0.0

    text = str(price_text)

    if "Free" in text:
        return 0.0

    cleaned = re.sub(r"[^\d.,]", "", text)
    cleaned = cleaned.replace(",", ".")

    try:
        numbers = re.findall(r"\d+\.\d+|\d+", cleaned)
        return float(numbers[0]) if numbers else 0.0
    except ValueError:
        return 0.0


def clean_discount(discount_text):
    """Convert discount percentage text into an integer."""

    if not discount_text:
        return 0

    numbers = re.findall(r"\d+", str(discount_text))
    return int(numbers[0]) if numbers else 0


def clean_platforms(platforms):
    """Normalize platform values into a clean list."""

    if isinstance(platforms, str):
        try:
            platforms = ast.literal_eval(platforms)
        except Exception:
            platforms = [item.strip() for item in platforms.split(",") if item.strip()]

    if not isinstance(platforms, list):
        return []

    cleaned = []
    for platform in platforms:
        if platform not in ["platform_img", "group_separator"]:
            cleaned.append(platform)

    return cleaned


def infer_game_type(price_numeric):
    return "Free" if price_numeric == 0 else "Paid"


def clean_dataframe(df):
    """Clean a Steam games DataFrame and enrich the dataset."""

    if df is None or df.empty:
        return pd.DataFrame()

    df = df.copy()

    df["price_numeric"] = (
        df["price"].apply(clean_price)
        if "price" in df.columns
        else 0.0
    )

    df["discount_numeric"] = (
        df["discount"].apply(clean_discount)
        if "discount" in df.columns
        else 0
    )

    if "platforms" in df.columns:
        df["platforms"] = df["platforms"].apply(clean_platforms)
    else:
        df["platforms"] = [[] for _ in range(len(df))]

    df["game_type"] = df["price_numeric"].apply(infer_game_type)
    df = df.drop_duplicates(subset=["title"]).reset_index(drop=True)

    return df


def load_data_from_csv(input_path="output/csv/steam_games_cleaned.csv"):
    if not os.path.exists(input_path):
        raise FileNotFoundError(
            f"Backup CSV file not found at {input_path}."
        )

    df = pd.read_csv(input_path)
    return df


def process_data(source="mongodb", fallback_csv=True):
    """Load cleaned data from MongoDB Atlas, with optional CSV fallback."""

    df = pd.DataFrame()

    if source == "mongodb":
        df = load_data_from_db()

        if not df.empty:
            print("Loaded dataset directly from MongoDB Atlas")

    if (df is None or df.empty) and fallback_csv:
        try:
            df = load_data_from_csv()
            print("Loaded dataset from backup CSV")
        except FileNotFoundError as error:
            print(error)
            df = pd.DataFrame()

    if df is None or df.empty:
        print("No data available to process.")
        return pd.DataFrame()

    df = clean_dataframe(df)

    print("Dataset Loaded Successfully")
    print(f"\nTotal Records: {len(df)}")
    print("\nDataset Preview:\n")
    print(
        df[["title", "price_numeric", "discount_numeric", "game_type"]].head(10)
    )

    return df


def save_cleaned_csv(df, output_path="output/csv/steam_games_cleaned.csv"):
    export_to_csv(df, output_path)


def run_business_analysis(df):
    if df is None or df.empty:
        print("No data available for analytics.")
        return

    print("\nBUSINESS ANALYTICS")
    print("=" * 60)

    average_price = df["price_numeric"].mean()
    print(f"\nAverage Game Price: €{average_price:.2f}")

    game_type_counts = df["game_type"].value_counts()
    print("\nFree vs Paid Games:\n")
    print(game_type_counts)

    print("\nTop 10 Most Expensive Games:\n")
    expensive_games = (
        df.sort_values(by="price_numeric", ascending=False)
        [["title", "price_numeric"]]
        .head(10)
    )
    print(expensive_games)

    print("\nTop 10 Highest Discounted Games:\n")
    discounted_games = (
        df.sort_values(by="discount_numeric", ascending=False)
        [["title", "discount_numeric"]]
        .head(10)
    )
    print(discounted_games)

    print("\nMost Common Platforms:\n")
    exploded_platforms = df.explode("platforms")
    platform_counts = exploded_platforms["platforms"].value_counts()
    print(platform_counts)

    print("\nBusiness Analytics Completed")


if __name__ == "__main__":
    cleaned_df = process_data()
    run_business_analysis(cleaned_df)