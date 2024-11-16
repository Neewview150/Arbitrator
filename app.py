from flask import Flask, jsonify, send_from_directory
import logging
from data_fetcher import fetch_symbols, fetch_market_data, prepare_chart_data
from arbitrage_finder import find_direct_arbitrage_opportunities, find_triangular_arbitrage_opportunities, format_arbitrage_opportunities, calculate_profitability_and_duration, fetch_executed_trades

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

@app.route('/')
def serve_interface():
    """Serve the HTML interface."""
    return send_from_directory('.', 'interface.html')

@app.route('/api/data', methods=['GET'])
def get_data():
    """API endpoint to fetch chart data and arbitrage opportunities."""
    try:
        # Load symbol mapping
        # Fetch symbols and prices using the private API
        try:
            symbols = fetch_symbols()
            prices = fetch_market_data()
            logging.info(f"Fetched symbols and prices using private API: {symbols}, {prices}")
        except Exception as e:
            logging.error(f"Error fetching symbols and prices using private API: {e}")
            return jsonify({'error': 'Failed to fetch symbols and prices using private API'}), 500
        
        # Prepare chart data
        chart_data = prepare_chart_data(prices)
        
        # Find arbitrage opportunities
        direct_arbitrage_opportunities = find_direct_arbitrage_opportunities(symbols, symbol_to_id, prices)
        triangular_arbitrage_opportunities = find_triangular_arbitrage_opportunities(symbols, symbol_to_id, prices)
        
        # Calculate additional information for arbitrage opportunities
        arbitrage_opportunities = direct_arbitrage_opportunities + triangular_arbitrage_opportunities
        arbitrage_opportunities = calculate_profitability_and_duration(arbitrage_opportunities)
        
        # Fetch executed trades
        executed_trades = fetch_executed_trades()
        
        # Format arbitrage opportunities
        formatted_arbitrage_opportunities = format_arbitrage_opportunities(arbitrage_opportunities)
        
        # Return data as JSON
        return jsonify({
            'prices': chart_data,
            'arbitrageOpportunities': formatted_arbitrage_opportunities,
            'executedTrades': executed_trades
        })
    except Exception as e:
        logging.error(f"Unexpected error in /api/data endpoint: {e}")
        return jsonify({'error': 'Unexpected error occurred'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
