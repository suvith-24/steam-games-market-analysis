import os
import matplotlib.pyplot as plt
import seaborn as sns

from analysis.analysis import clean_dataframe
from database.mongodb_connection import load_data_from_db


os.makedirs("output/charts", exist_ok=True)


def load_data():
    df = load_data_from_db()

    if df.empty:
        print("No data found in MongoDB Atlas for visualization.")
        return df

    return clean_dataframe(df)


def free_vs_paid_chart(df):
    plt.figure(figsize=(6, 6))

    counts = df["game_type"].value_counts()

    counts.plot(kind="pie", autopct="%1.1f%%")

    plt.title("Free vs Paid Games")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig("output/charts/free_vs_paid.png")
    plt.close()

    print("Free vs Paid Chart Saved")


def platform_chart(df):
    exploded = df.explode("platforms")
    platform_counts = exploded["platforms"].value_counts().head(10)

    plt.figure(figsize=(8, 6))
    sns.barplot(
        x=platform_counts.index,
        y=platform_counts.values,
        color="#2a9d8f"
    )

    plt.title("Most Common Platforms")
    plt.xlabel("Platform")
    plt.ylabel("Number of Games")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("output/charts/platforms.png")
    plt.close()

    print("Platform Chart Saved")


def discount_chart(df):
    top_discounts = df.sort_values(
        by="discount_numeric",
        ascending=False
    ).head(10)

    plt.figure(figsize=(10, 6))
    sns.barplot(
        x="discount_numeric",
        y="title",
        data=top_discounts,
        color="#e76f51"
    )

    plt.title("Top Discounted Games")
    plt.xlabel("Discount Percentage")
    plt.ylabel("Game Title")
    plt.tight_layout()
    plt.savefig("output/charts/top_discounts.png")
    plt.close()

    print("Discount Chart Saved")


def expensive_games_chart(df):
    expensive_games = df.sort_values(
        by="price_numeric",
        ascending=False
    ).head(10)

    plt.figure(figsize=(10, 6))
    sns.barplot(
        x="price_numeric",
        y="title",
        data=expensive_games,
        color="#264653"
    )

    plt.title("Most Expensive Games")
    plt.xlabel("Price (€)")
    plt.ylabel("Game Title")
    plt.tight_layout()
    plt.savefig("output/charts/expensive_games.png")
    plt.close()

    print("Expensive Games Chart Saved")


def generate_visualizations(df=None):
    print("\nGenerating Visualizations...\n")

    if df is None:
        df = load_data()

    if df is None or df.empty:
        print("Visualization skipped because no data is available.")
        return

    free_vs_paid_chart(df)
    platform_chart(df)
    discount_chart(df)
    expensive_games_chart(df)

    print("\nAll Charts Generated Successfully")


if __name__ == "__main__":
    generate_visualizations()