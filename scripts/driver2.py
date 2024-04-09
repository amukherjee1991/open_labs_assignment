from MarketDepthCalculator import MarketDepthCalculator
import pandas as pd

def main():
    # Load dataset
    dataset_path = 'data/openblocks.parquet'
    dataset = pd.read_parquet(dataset_path)
    print(dataset.columns)

    # # Dummy pair prices (replace with real prices or fetch from CoinGecko)
    # dummy_pair_prices = {'STRK/ETH': 0.03, 'STRK/USDC': 20, 'ETH/USDC': 2000, 'USDC/USDT': 1}

    # md_calculator = MarketDepthCalculator(dataset)
    # price_ratios = md_calculator.calculate_price_ratios()
    # print(price_ratios)
    # price_ratios.to_csv("data/price_rations.csv",index=False)

    # # Store liquidity based on tick deltas (simplified version)
    # liquidity_info = md_calculator.store_liquidity()
    # print(liquidity_info.head())

    # # Calculate market depths (needs to be implemented based on specific logic)
    # market_depths = md_calculator.calculate_market_depths(dummy_pair_prices)
    # print(market_depths)
    # # Proceed with other steps...

if __name__ == "__main__":
    main()
