from coingecko_client import CoinGeckoClient
from MarketDepthCalculator import MarketDepthCalculator
import pandas as pd

def main():
    # Initialize the CoinGecko client and fetch pair prices
    cg_client = CoinGeckoClient()
    pair_prices = cg_client.fetch_pair_prices()

    # Load the dataset
    dataset_path = 'data/openblocks.parquet'
    dataset = pd.read_parquet(dataset_path)

    # Print the fetched pair prices
    print("Fetched Pair Prices:")
    for pair, price in pair_prices.items():
        print(f"{pair}: {price}")

if __name__ == "__main__":
    main()
