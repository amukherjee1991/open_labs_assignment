# coingecko_client.py

from pycoingecko import CoinGeckoAPI

class CoinGeckoClient:
    def __init__(self):
        self.cg = CoinGeckoAPI()

    def fetch_pair_prices(self):
        prices = self.cg.get_price(ids=['strike', 'ethereum', 'usd-coin', 'tether'], vs_currencies='usd')
        pair_prices = {
            'STRK/ETH': prices['strike']['usd'] / prices['ethereum']['usd'],
            'STRK/USDC': prices['strike']['usd'] / prices['usd-coin']['usd'],
            'ETH/USDC': prices['ethereum']['usd'] / prices['usd-coin']['usd'],
            'USDC/USDT': prices['usd-coin']['usd'] / prices['tether']['usd']
        }
        return pair_prices

if __name__ == "__main__":
    cg = CoinGeckoClient()
    pair_data = cg.fetch_pair_prices()
    print(pair_data)