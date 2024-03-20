import requests
import pandas as pd

class CoinGeckoPrices:
    def __init__(self, coins):
        """
        Initialize with a dictionary mapping the coin's ticker in uppercase 
        to its CoinGecko ID.
        """
        self.coins = coins  # This should now be a dict
        self.base_url = "https://api.coingecko.com/api/v3/simple/price"
    
    def fetch_prices(self):
        """
        Fetches the current prices for the specified coins.
        """
        # Use the values of the dict (CoinGecko IDs) for querying
        ids = ','.join(self.coins.values())  
        url = f"{self.base_url}?ids={ids}&vs_currencies=usd"
        response = requests.get(url)
        price_data = response.json()
        
        # Extract the coin tickers (in uppercase as keys of the dict) and their prices in USD
        prices = [{'coin': ticker, 'price': price_data[coin_id]['usd'] if coin_id in price_data else 'Not Available'} 
                  for ticker, coin_id in self.coins.items()]
                
        return prices
    
    def save_prices_to_csv(self, file_path):
        """
        Saves the fetched coin prices to a CSV file.

        Parameters:
        - file_path: Path to save the CSV file, including the filename.
        """
        prices = self.fetch_prices()
        prices_df = pd.DataFrame(prices)
        prices_df.to_csv(file_path, index=False)
        print(f"Prices saved to {file_path}")

# Mapping of coin tickers in uppercase to their CoinGecko IDs
# coins = {
#     'STRK': 'starknet',
#     'ETH': 'ethereum',
#     'USDC': 'usd-coin',
#     'USDT': 'tether'
# }

# cg_prices = CoinGeckoPrices(coins)

# # Specify the folder and filename where you want to save the CSV
# file_path = './data/token_price.csv'

# # Fetch the current prices and save them to the specified CSV file
# cg_prices.save_prices_to_csv(file_path)
