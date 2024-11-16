# Arbitrator

## Introduction

Arbitrator is a tool designed to identify and exploit arbitrage opportunities in cryptocurrency markets. It fetches real-time price data from multiple exchanges and analyzes it to find both direct and triangular arbitrage opportunities. The project includes a web interface to visualize trading data and arbitrage opportunities using dynamic charts.

## Installation

To set up the project, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Neewview150/Arbitrator.git
   cd Arbitrator
   ```

2. **Set up a virtual environment** (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scriptsctivate`
   ```

3. **Install the dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
## API Credentials Setup

To use the private API for fetching price data, you need to set up your API credentials. Follow these steps:

1. Obtain your API key and secret from the exchange or service you are using.
2. Set the API credentials as environment variables in your system:

   - On macOS and Linux:
     ```bash
     export API_KEY='your_api_key_here'
     export API_SECRET='your_api_secret_here'
     ```

   - On Windows:
     ```cmd
     set API_KEY=your_api_key_here
     set API_SECRET=your_api_secret_here
     ```

   Alternatively, you can create a `.env` file in the project root directory and add the following lines:
   ```
   API_KEY=your_api_key_here
   API_SECRET=your_api_secret_here
   ```

   Make sure to replace `your_api_key_here` and `your_api_secret_here` with your actual API key and secret.

## Usage
To run the project and start the web interface, execute the following command:

```bash
python app.py
```

This will start a local server. Open your web browser and navigate to `http://localhost:5000` to access the interface. Here, you can view charts of trading data and a list of current arbitrage opportunities.

## Contributing

Contributions are welcome! If you would like to contribute to this project, please follow these guidelines:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them with clear and descriptive messages.
4. Push your changes to your forked repository.
5. Submit a pull request to the main repository.

Please ensure your code adheres to the project's coding standards and includes appropriate tests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
