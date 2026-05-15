import os
from pathlib import Path
from dotenv import load_dotenv
import pandas as pd
from pymongo import MongoClient, UpdateOne
from pymongo.errors import BulkWriteError

load_dotenv()

MONGO_DB_NAME = "steam_games_db"
MONGO_COLLECTION_NAME = "steam_games"
CSV_BACKUP_PATH = Path("output/csv/steam_games_cleaned.csv")


def get_mongo_uri():
    mongo_uri = os.getenv("MONGO_URI")

    if not mongo_uri:
        raise EnvironmentError(
            "MONGO_URI is not set. Please add it to .env."
        )

    return mongo_uri


def connect_mongodb():
    """Connect to MongoDB Atlas and return a client."""

    try:
        mongo_uri = get_mongo_uri()

        client = MongoClient(
            mongo_uri,
            serverSelectionTimeoutMS=5000
        )

        client.admin.command("ping")

        print("Successfully connected to MongoDB Atlas")

        return client

    except Exception as e:
        print(f"MongoDB Connection Error: {e}")
        return None


def get_collection():
    client = connect_mongodb()

    if client is None:
        return None, None

    db = client[MONGO_DB_NAME]
    collection = db[MONGO_COLLECTION_NAME]
    ensure_indexes(collection)

    return client, collection


def ensure_indexes(collection):
    """Create indexes that make duplicate prevention and queries efficient."""

    try:
        collection.create_index(
            "title",
            unique=True,
            name="unique_title_index"
        )

        collection.create_index(
            "platforms",
            name="platforms_index"
        )
    except Exception as e:
        print(f"Index creation warning: {e}")


def load_data_from_db(limit=None):
    client, collection = get_collection()

    if collection is None:
        return pd.DataFrame()

    try:
        query = collection.find({}, {"_id": 0})

        if limit is not None:
            query = query.limit(limit)

        documents = list(query)

        if not documents:
            return pd.DataFrame()

        return pd.DataFrame(documents)

    except Exception as e:
        print(f"Error loading data from MongoDB: {e}")
        return pd.DataFrame()

    finally:
        client.close()


def upsert_games(games_list):
    if not games_list:
        print("No records to insert into MongoDB.")
        return

    client, collection = get_collection()

    if collection is None:
        return

    try:
        operations = [
            UpdateOne(
                {"title": game["title"]},
                {"$set": game},
                upsert=True
            )
            for game in games_list
        ]

        result = collection.bulk_write(
            operations,
            ordered=False
        )

        inserted = getattr(result, "upserted_count", 0)
        modified = getattr(result, "modified_count", 0)

        print("\nMONGODB UPSERT SUMMARY")
        print("-" * 50)
        print(f"New Documents Inserted: {inserted}")
        print(f"Existing Documents Updated: {modified}")
        print(
            f"Total Documents in MongoDB: "
            f"{collection.count_documents({})}"
        )
        print("\nData successfully stored in MongoDB Atlas")

    except BulkWriteError as bulk_error:
        print(f"Bulk write warning: {bulk_error.details}")
    except Exception as e:
        print(f"Insertion Error: {e}")
    finally:
        client.close()


def export_to_csv(df, output_path=CSV_BACKUP_PATH):
    try:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_path, index=False)
        print(f"Cleaned dataset exported to {output_path}")
    except Exception as e:
        print(f"CSV export failed: {e}")
