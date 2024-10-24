import logging
from data_fetcher import fetch_and_return_data

def find_direct_arbitrage_opportunities(symbols, symbol_to_id, prices):
    """Find direct arbitrage opportunities between exchanges."""
    arbitrage_opportunities = []
    for symbol in symbols:
        for exchange1 in exchanges:
            for exchange2 in exchanges:
                if exchange1 != exchange2:
                    price1 = prices[symbol][exchange1]
                    price2 = prices[symbol][exchange2]
                    if price1 > price2:
                        arbitrage_opportunities.append((symbol, exchange1, exchange2, price1, price2))
    return arbitrage_opportunities

def find_triangular_arbitrage_opportunities(symbols, symbol_to_id, prices, fee_percentage=0.002):
    """Find triangular arbitrage opportunities between exchanges, ensuring all symbols are distinct."""
    triangular_arbitrage_opportunities = []
    
    for symbol1 in symbols:
        for symbol2 in symbols:
            for symbol3 in symbols:
                # Ensure all symbols are distinct
                if symbol1 != symbol2 and symbol2 != symbol3 and symbol1 != symbol3:
                    for exchange1 in exchanges:
                        for exchange2 in exchanges:
                            for exchange3 in exchanges:
                                # Ensure all exchanges are distinct
                                if exchange1 != exchange2 and exchange2 != exchange3 and exchange1 != exchange3:
                                    price1 = prices[symbol1][exchange1]
                                    price2 = prices[symbol2][exchange2]
                                    price3 = prices[symbol3][exchange3]

                                    if price1 > 0 and price2 > 0 and price3 > 0:
                                        # Calculate potential profit without fees
                                        profit_without_fees = (price1 / price2) * price3
                                        
                                        # Apply fees
                                        total_fee = (fee_percentage * (price1 + price2 + price3))
                                        profit_with_fees = profit_without_fees - total_fee
                                        
                                        # Check if the profit is positive after fees
                                        if profit_with_fees > 0:
                                            profit_percentage = (profit_with_fees / total_fee) * 100
                                            if profit_percentage > 1:  # Set a threshold for profitability
                                                triangular_arbitrage_opportunities.append(
                                                    (symbol1, symbol2, symbol3, exchange1, exchange2, exchange3, price1, price2, price3, profit_with_fees)
                                                )
    return triangular_arbitrage_opportunities

def simulate_trade(symbol1, symbol2, symbol3, exchange1, exchange2, exchange3, price1, price2, price3, fee_percentage):
    """Simulate a triangular trade and return the profit amount."""
    # Assume starting with 1 unit of symbol2
    investment = 1.0  # Starting with 1 unit of symbol2

    # Step 1: Buy symbol1 using symbol2 on exchange2
    amount_symbol1 = investment / price2  # Amount of symbol1 we can buy
    cost_symbol1 = amount_symbol1 * price2 * (1 + fee_percentage)  # Cost including fee on exchange2

    # Step 2: Buy symbol 3 using symbol1 on exchange1
    amount_symbol3 = amount_symbol1 * price1  # Amount of symbol3 we can buy
    cost_symbol3 = amount_symbol3 * price1 * (1 + fee_percentage)  # Cost including fee on exchange1

    # Step 3: Sell symbol3 for symbol2 on exchange3
    final_amount_symbol2 = amount_symbol3 * (price3 * (1 - fee_percentage))  # Amount of symbol2 after selling

    # Calculate profit
    profit = final_amount_symbol2 - investment  # Profit from the trade

    return profit  # Return the profit amount

def write_successful_arbitrages_to_file(opportunities):
    """Write successful arbitrage opportunities to a text file."""
    with open("arbitrage_opportunities.txt", "w") as file:
        for opportunity in opportunities:
            file.write(f"{opportunity}\n")

if __name__ == "__main__":
    symbols, prices, symbol_to_id = fetch_and_return_data("symbols.txt")
    direct_arbitrage_opportunities = find_direct_arbitrage_opportunities(symbols, symbol_to_id, prices)
    triangular_arbitrage_opportunities = find_triangular_arbitrage_opportunities(symbols, symbol_to_id, prices)
    write_successful_arbitrages_to_file(direct_arbitrage_opportunities + triangular_arbitrage_opportunities)