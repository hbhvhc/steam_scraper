import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of Steam's Specials (Discounted) Games Page with USD Currency (US Region)
URL = "https://store.steampowered.com/search/?specials=1&cc=us"

# Send a GET request to fetch the HTML content of the page
response = requests.get(URL)

# Check if the request was successful (Status code 200)
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the containers of each game
    games = soup.find_all('a', class_='search_result_row')

    # Prepare lists to store game data
    game_titles = []
    original_prices = []
    discounted_prices = []
    discounts = []

    # Loop through the games found and extract data
    for game in games:
        # Error handling for missing title
        title = game.find('span', class_='title')
        title = title.text.strip() if title else 'N/A'  # Fallback to 'N/A' if title not found

        # Error handling for missing discount
        discount_percent = game.find('div', class_='search_discount')
        discount_percent = discount_percent.text.strip() if discount_percent else 'No Discount'

        # Error handling for missing price
        price_info = game.find('div', class_='search_price')
        price_info = price_info.text.strip() if price_info else 'N/A'

        # Separate original and discounted prices if both are available
        if discount_percent != 'No Discount':
            prices = price_info.split('$')
            if len(prices) > 2:
                original_price = f"${prices[1].strip()}"
                discounted_price = f"${prices[2].strip()}"
            elif len(prices) > 1:
                original_price = f"${prices[0].strip()}"
                discounted_price = f"${prices[1].strip()}"
            else:
                original_price = price_info
                discounted_price = price_info
        else:
            original_price = price_info
            discounted_price = price_info

        # Append the extracted data to the lists
        game_titles.append(title)
        original_prices.append(original_price)
        discounted_prices.append(discounted_price)
        discounts.append(discount_percent)

    # Create a DataFrame to organize the data
    data = {
        'Title': game_titles,
        'Original Price': original_prices,
        'Discounted Price': discounted_prices,
        'Discount Percentage': discounts
    }

    df = pd.DataFrame(data)

    # Display the DataFrame (for terminal use)
    print(df)

    # Optionally, save the data to a CSV file
    df.to_csv('steam_discounted_games_usd.csv', index=False)
else:
    print(f"Failed to retrieve data: {response.status_code}")
