
# Crypto Token Pair Analysis Tool

This Python script provides a comprehensive analysis tool for examining cryptocurrency token pairs. It's designed to assess market depth and profit-and-loss (PnL) calculations based on historical transaction data. This script is especially useful for researchers, traders, and analysts looking to understand the liquidity and performance of specific token pairs in the cryptocurrency market.

## Features

- **Load Data:** Capable of loading datasets from Parquet files, ensuring efficient processing of large volumes of data.
- **Token Price Fetching:** Utilizes the `CoinGeckoPrices` class to fetch current prices of tokens from CoinGecko, storing the data in CSV format.
- **Token Addresses:** Found the unique addresses belonging to tokens and simple google search revealed which contract address belongs to which coin. Created a json file to map them.
- **Market Depth Calculation:** Calculates the market depth of token pairs by summing the absolute liquidity amounts and averaging the prices of the tokens involved.
- **Profit and Loss (PnL) Calculation:** Estimates the PnL for individual tokens within a pair based on initial prices, final prices, and initial liquidity.
- **Token Pair Filtering:** Analyzes transactions for specified token pairs, filtering the data to include only relevant transactions.
- **Command Line Interface:** Allows users to specify the data directory through command line arguments, making the tool flexible and easy to integrate into various workflows.

## Usage

1. **Setup:** Ensure all dependencies are installed, including `pandas`, `json`, and `decimal` among others. The `CoinGeckoPrices` class needs to be defined elsewhere in your project.
2. **Command Line Argument:** The script accepts a single command line argument specifying the directory containing the data files. Example: `python script.py ./data`
3. **Data Files:** Prepare your dataset in the following formats:
   - **Dataset:** A Parquet file containing transaction data.
   - **Token Prices:** A CSV file with the current prices of tokens. (downloaded from coingecko)
   - **Token Addresses:** A JSON file with token addresses. (found manually)

## Analyzing Token Pairs

Specify the token pairs you want to analyze in the `token_pairs` list within the script. For each pair, the script will:
- Filter relevant transactions from the dataset.
- Calculate the market depth.
- Estimate the PnL for each token in the pair.

Results for each token pair are printed to the console, including market depth and PnL calculations.

## Extensibility

The script is designed for extensibility, allowing users to add more token pairs, adjust the PnL calculation logic, or integrate additional data sources for price fetching.
