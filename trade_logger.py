import logging

def setup_logger():
    """Set up the logger to write to a file and overwrite it each time."""
    logging.basicConfig(
        filename='trade_log.txt',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filemode='w'  # Overwrite the log file each time
    )

def log_trade(trade_info):
    """Log trade details."""
    logging.info(f"Trade executed: {trade_info}")

def log_error(error_message):
    """Log an error message."""
    logging.error(f"Error: {error_message}")

def log_debug(debug_message):
    """Log a debug message."""
    logging.debug(f"Debug: {debug_message}")

# Initialize the logger when the module is imported
setup_logger()
