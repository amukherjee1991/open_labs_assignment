import pandas as pd
import numpy as np
from coingecko_client import CoinGeckoClient
class MarketDepthCalculator:
    def __init__(self, dataset):
        self.dataset = dataset
        # Ensure the dataset is prepared for calculations
        self.prepare_dataset()

    def prepare_dataset(self):
        # Convert amounts to numeric and handle any necessary preprocessing
        self.dataset['TOKEN0_REAL_AMOUNT'] = pd.to_numeric(self.dataset['TOKEN0_REAL_AMOUNT'], errors='coerce')
        self.dataset['TOKEN1_REAL_AMOUNT'] = pd.to_numeric(self.dataset['TOKEN1_REAL_AMOUNT'], errors='coerce')

    def calculate_price_ratios(self):
        # Filter out records where TOKEN1_REAL_AMOUNT is zero to avoid division by zero
        valid_ratios = self.dataset[self.dataset['TOKEN1_REAL_AMOUNT'] != 0]
        # Calculate price ratio
        valid_ratios['price_ratio'] = valid_ratios['TOKEN0_REAL_AMOUNT'] / valid_ratios['TOKEN1_REAL_AMOUNT']
        
        # Aggregate to find average price ratio per pool if necessary
        # This assumes that an average might be meaningful for your analysis
        price_ratios = valid_ratios.groupby('POOL_ID')['price_ratio'].mean().reset_index()
        return price_ratios

    def store_liquidity(self):
        # Create a data structure that summarizes liquidity changes at each tick
        # For simplicity, here we're just aggregating LIQUIDITY_AMOUNT by LOWER_TICK and UPPER_TICK within each POOL_ID
        liquidity_summary = self.dataset.groupby(['POOL_ID', 'LOWER_TICK', 'UPPER_TICK'])['LIQUIDITY_AMOUNT'].sum().reset_index()
        return liquidity_summary
    

    def liquidity_in_range(self, pool_id, lower_price, upper_price):
        # Filter dataset for the specified pool
        pool_data = self.dataset[self.dataset['POOL_ID'] == pool_id]
        
        # Placeholder logic to determine if a tick falls within the price range
        # This should be replaced with actual logic based on your tick-to-price conversion
        in_range_ticks = pool_data[(pool_data['LOWER_TICK'] >= lower_price) & (pool_data['UPPER_TICK'] <= upper_price)]
        
        # Sum the liquidity amounts for ticks within the range
        total_liquidity = in_range_ticks['LIQUIDITY_AMOUNT'].sum()
        
        return total_liquidity
    
    def calculate_market_depths(self, pair_prices):
        market_depths = {}
        for pair, current_price in pair_prices.items():
            depths = {'1%': 0, '5%': 0, '10%': 0}
            
            for percentage in depths:
                price_percentage = float(percentage.strip('%')) / 100
                upper_price = current_price * (1 + price_percentage)
                lower_price = current_price * (1 - price_percentage)
                
                # Corrected iteration over pool IDs and calculation for each
                for pool_id in self.dataset['POOL_ID'].unique():
                    liquidity = self.liquidity_in_range(pool_id, lower_price, upper_price)
                    
                    # Accumulate the calculated liquidity for the depth percentage across all pools
                    depths[percentage] += liquidity
            
            market_depths[pair] = depths
        
        return market_depths

# Example usage with dummy data and steps execution
if __name__ == "__main__":
    # Load your dataset here
    dataset_path = 'data/openblocks.parquet'
    dataset = pd.read_parquet(dataset_path)
    calculator = MarketDepthCalculator(dataset)
    cg = CoinGeckoClient()
    pair_data = cg.fetch_pair_prices()
    print(pair_data)

    # Calculate and print price ratios
    price_ratios = calculator.calculate_price_ratios()
    print("Price Ratios:\n", price_ratios.head())
    
    # Store and print aggregated liquidity information
    liquidity_info = calculator.store_liquidity()
    print("Aggregated Liquidity Info:\n", liquidity_info.head())

    # Dummy pair prices for calculation; replace with real data or fetch using CoinGeckoClient if applicable
    dummy_pair_prices = {
        'STRK/ETH': 0.03,  # Assume this price is for demonstration; actual price will vary
        'STRK/USDC': 20,
        'ETH/USDC': 2000,
        'USDC/USDT': 1
    }

    # Calculate and print market depths for the specified pairs
    market_depths = calculator.calculate_market_depths(pair_data)
    print("Market Depths:\n", market_depths)
