import pandas as pd
import json
from decimal import Decimal
import random
import argparse
from coingecko_prices import CoinGeckoPrices

# Import other necessary modules here (e.g., CoinGeckoPrices)

# Assuming CoinGeckoPrices and other necessary imports are defined elsewhere in your project


# Function to load the dataset
def load_dataset(file_path):
    """Loads the dataset from a specified Parquet file."""
    df = pd.read_parquet(file_path)
    return df


# Function to load token prices from CSV
def load_token_prices(file_path):
    """Loads token prices from a specified CSV file."""
    df = pd.read_csv(file_path)
    prices = {row["coin"]: Decimal(row["price"]) for index, row in df.iterrows()}
    return prices


# Function to load token addresses from JSON
def load_token_addresses(file_path):
    """Loads token addresses from a specified JSON file."""
    with open(file_path, "r") as file:
        addresses = json.load(file)
    return addresses


# Function to calculate market depth
def calculate_market_depth(pool_df, token_prices):
    """Calculate market depth for a given pool DataFrame."""
    total_liquidity = pool_df["LIQUIDITY_AMOUNT"].abs().sum()
    avg_token_price = Decimal(sum(token_prices.values()) / len(token_prices))
    market_depth_usd = total_liquidity * avg_token_price
    return market_depth_usd


# Function to calculate PnL for single initial and final prices with liquidity
def calculate_pnl_single(initial_price, final_price, initial_liquidity):
    """Calculate PnL based on initial and final prices and initial liquidity."""
    pnl = (final_price - initial_price) * initial_liquidity
    return pnl


# Function to filter transactions for a specific token pair
def filter_pool_transactions_and_find_pool_id(df, token0, token1, token_addresses):
    """Filters the DataFrame for transactions involving the specified token pair and finds pool IDs."""
    token0_address = token_addresses[token0].lower()
    token1_address = token_addresses[token1].lower()
    pool_df = df[
        (
            (df["TOKEN0_ADDRESS"].str.lower() == token0_address)
            & (df["TOKEN1_ADDRESS"].str.lower() == token1_address)
        )
        | (
            (df["TOKEN0_ADDRESS"].str.lower() == token1_address)
            & (df["TOKEN1_ADDRESS"].str.lower() == token0_address)
        )
    ]
    return pool_df["POOL_ID"].unique(), pool_df


# Main function with argparse for data directory
def main():
    # Setup argument parser
    parser = argparse.ArgumentParser(
        description="Analyze Token Pairs Market Depth and PnL"
    )
    parser.add_argument(
        "data_directory", type=str, help="Directory containing the data files"
    )
    args = parser.parse_args()

    # Construct file paths using provided data_directory argument
    dataset_path = f"{args.data_directory}/openblocks.parquet"
    addresses_file_path = f"{args.data_directory}/token_addresses.json"
    prices_file_path = f"{args.data_directory}/token_price.csv"

    # Load dataset
    df = load_dataset(dataset_path)

    # Specify the coins and their IDs for fetching prices
    coins = {
        "STRK": "starknet",
        "ETH": "ethereum",
        "USDC": "usd-coin",
        "USDT": "tether",
    }

    # Initialize CoinGeckoPrices to fetch current prices
    cg_prices = CoinGeckoPrices(coins)
    cg_prices.save_prices_to_csv(prices_file_path)

    # Load current token prices from the updated CSV
    token_prices = load_token_prices(prices_file_path)

    # Load token addresses
    token_addresses = load_token_addresses(addresses_file_path)

    # Specify the token pairs
    token_pairs = [
        ("STRK", "ETH"),
        ("STRK", "USDC"),
        ("ETH", "USDC"),
        ("USDC", "USDT"),
    ]

    for token0, token1 in token_pairs:
        print(f"Analyzing pair: {token0}/{token1}")

        # Filter transactions for the specified token pair
        unique_pool_ids, pool_df = filter_pool_transactions_and_find_pool_id(
            df, token0, token1, token_addresses
        )

        if not pool_df.empty:
            # Calculate and display market depth
            # Calculate and display market depth
            prices_for_pair = {
                token0: token_prices[token0],
                token1: token_prices[token1],
            }
            market_depth = calculate_market_depth(pool_df, prices_for_pair)
            print(f"Market Depth (USD) for {token0}/{token1}: {market_depth:.2f}")

            # Calculate and display PnL - Using hardcoded initial prices for demonstration
            initial_prices = {
                token: Decimal(random.randint(50, 150)) for token in [token0, token1]
            }  # Random initial prices
            initial_liquidity = Decimal("1000")  # Hypothetical initial liquidity
            final_prices = prices_for_pair  # Final prices from CoinGecko

            # Corrected PnL calculation for single token
            pnl_token0 = calculate_pnl_single(
                initial_prices[token0], final_prices[token0], initial_liquidity
            )
            pnl_token1 = calculate_pnl_single(
                initial_prices[token1], final_prices[token1], initial_liquidity
            )
            total_pnl = pnl_token0 + pnl_token1

            print(
                f"PnL for {token0}: {pnl_token0:.2f}, {token1}: {pnl_token1:.2f}, Total: {total_pnl:.2f}\n"
            )

        else:
            print(f"No data found for pool {token0}/{token1}.")


if __name__ == "__main__":
    main()
