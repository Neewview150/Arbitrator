from flask import Flask, jsonify, send_from_directory
import logging
from data_fetcher import fetch_and_return_data, prepare_chart_data
from arbitrage_finder import find_direct_arbitrage_opportunities, find_triangular_arbitrage_opportunities, format_arbitrage_opportunities

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
        symbol_to_id = fetch_and_return_data("symbols.txt")
        
        # Fetch symbols and prices
        symbols, prices = fetch_and_return_data(symbol_to_id)
        
        # Prepare chart data
        chart_data = prepare_chart_data(prices)
        
        # Find arbitrage opportunities
        direct_arbitrage_opportunities = find_direct_arbitrage_opportunities(symbols, symbol_to_id, prices)
        triangular_arbitrage_opportunities = find_triangular_arbitrage_opportunities(symbols, symbol_to_id, prices)
        
        # Format arbitrage opportunities
        arbitrage_opportunities = format_arbitrage_opportunities(direct_arbitrage_opportunities + triangular_arbitrage_opportunities)
        
        # Return data as JSON
        return jsonify({
            'prices': chart_data,
            'arbitrageOpportunities': arbitrage_opportunities
        })
    except Exception as e:
        logging.error(f"Error fetching data: {e}")
        return jsonify({'error': 'Failed to fetch data'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
