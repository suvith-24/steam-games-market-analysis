import requests
from bs4 import BeautifulSoup
import time


def scrape_steam_games(page_count=80, delay=2):
    """Scrape Steam search pages and return a list of game dictionaries."""

    games_data = []

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        )
    }

    for page in range(page_count):
        start = page * 50
        url = (
            f"https://store.steampowered.com/search/"
            f"?supportedlang=english&start={start}"
        )

        print(f"\nScraping Page {page + 1}/{page_count}")
        print(f"Start Position: {start}")

        try:
            response = requests.get(
                url,
                headers=headers,
                timeout=15
            )

            if response.status_code != 200:
                print(f"Request Failed ({response.status_code})")
                continue

            soup = BeautifulSoup(response.text, "html.parser")
            games = soup.find_all("a", class_="search_result_row")

            print(f"Games Found: {len(games)}")

            for game in games:
                title_tag = game.find("span", class_="title")
                title = title_tag.text.strip() if title_tag else "No Title"

                discount_tag = game.find("div", class_="discount_pct")
                discount = discount_tag.text.strip() if discount_tag else "0%"

                price_tag = game.find("div", class_="discount_final_price")
                if not price_tag:
                    price_tag = game.find("div", class_="search_price")
                price = price_tag.text.strip() if price_tag else "Free"

                release_tag = game.find("div", class_="search_released")
                release_date = (
                    release_tag.text.strip()
                    if release_tag
                    else "Unknown"
                )

                platform_tags = game.find_all(
                    "span",
                    class_="platform_img"
                )

                platforms = []
                for platform in platform_tags:
                    classes = platform.get("class", [])
                    for cls in classes:
                        if cls != "platform_img":
                            platforms.append(cls)

                games_data.append({
                    "title": title,
                    "discount": discount,
                    "price": price,
                    "release_date": release_date,
                    "platforms": platforms
                })

            print(f"Total Games Collected So Far: {len(games_data)}")
            time.sleep(delay)

        except Exception as e:
            print(f"Error: {e}")

    return games_data


if __name__ == "__main__":
    data = scrape_steam_games()

    print("\nSCRAPING FINISHED")
    print(f"Total Games Scraped: {len(data)}")
    print("\nFirst 5 Games:\n")

    for game in data[:5]:
        print(game)
        print("-" * 60)