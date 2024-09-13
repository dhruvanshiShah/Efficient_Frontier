import os
import numpy as np
import datetime as dt
import argparse
import yaml
from utils.data_processing import get_stock_data
from utils.optimization import (
    maximize_sharpe_ratio,
    minimize_volatility,
    efficient_optimization,
    calculate_portfolio_performance,
)
from utils.visualization import plot_efficient_frontier

def load_config(config_file):
    """
    Loads configuration settings from a YAML file.

    Args:
        config_file (str): Path to the configuration file.

    Returns:
        dict: Configuration settings as a dictionary.
    """
def load_config(config_file):
    """
    Loads configuration settings from a YAML file.

    Args:
        config_file (str): Path to the configuration file.

    Returns:
        dict: Configuration settings as a dictionary.
    """
    try:
        # Ensure the path is relative to the script location
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(script_dir, config_file)
        
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        return config
    except Exception as e:
        print(f"Error loading configuration file: {e}")
        return {}


def parse_arguments():
    """
    Parses command-line arguments to override default configurations.

    Returns:
        argparse.Namespace: Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Portfolio Optimization")
    parser.add_argument(
        "--config", type=str, default="config.yaml", help="Path to the configuration file."
    )
    parser.add_argument(
        "--stocks",
        type=str,
        nargs="+",
        help="List of stock ticker symbols (space-separated).",
    )
    parser.add_argument(
        "--start-date",
        type=str,
        help="Start date for fetching data (format: YYYY-MM-DD).",
    )
    parser.add_argument(
        "--end-date",
        type=str,
        help="End date for fetching data (format: YYYY-MM-DD).",
    )
    parser.add_argument(
        "--risk-free-rate",
        type=float,
        help="Risk-free rate of return (e.g., 0.01 for 1%).",
    )
    return parser.parse_args()


def main():
    # Parse command-line arguments
    args = parse_arguments()

    # Load configurations from the file
    config = load_config(args.config)

    # Override configurations with command-line arguments if provided
    stock_symbols = args.stocks or config.get("stocks", ["AMZN", "AAPL", "MSFT", "GOOGL"])
    start_date = args.start_date or config.get("start_date", "2015-01-01")
    end_date = args.end_date or config.get("end_date", "2024-01-01")
    risk_free_rate = args.risk_free_rate or config.get("risk_free_rate", 0.01)

    # Convert date strings to datetime objects
    start_date = dt.datetime.strptime(start_date, "%Y-%m-%d")
    end_date = dt.datetime.strptime(end_date, "%Y-%m-%d")

    # Fetch data
    mean_returns, covariance_matrix = get_stock_data(stock_symbols, start_date, end_date)
    if mean_returns is None or covariance_matrix is None:
        print("Failed to fetch stock data. Exiting.")
        return

    # Maximize Sharpe ratio
    max_sharpe_result = maximize_sharpe_ratio(mean_returns, covariance_matrix, risk_free_rate)
    max_sharpe_performance = calculate_portfolio_performance(
        max_sharpe_result.x, mean_returns, covariance_matrix
    )

    # Minimize volatility
    min_vol_result = minimize_volatility(mean_returns, covariance_matrix)
    min_vol_performance = calculate_portfolio_performance(
        min_vol_result.x, mean_returns, covariance_matrix
    )

    # Efficient frontier calculation
    target_returns = np.linspace(min_vol_performance[1], max_sharpe_performance[1], 50)
    efficient_volatilities = [
        efficient_optimization(mean_returns, covariance_matrix, r).fun for r in target_returns
    ]

    # Plot the results
    plot_efficient_frontier(
        max_sharpe_performance, min_vol_performance, efficient_volatilities, target_returns
    )


if __name__ == "__main__":
    main()