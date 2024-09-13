import yfinance as yf
import pandas as pd


def get_stock_data(stock_symbols, start_date, end_date):
    """
    Fetches historical stock data and calculates mean returns and covariance matrix.

    Args:
        stock_symbols (list): List of stock ticker symbols.
        start_date (datetime): Start date for fetching data.
        end_date (datetime): End date for fetching data.

    Returns:
        tuple: Mean returns and covariance matrix of the stocks.
    """
    try:
        # Download historical stock data using yfinance
        stock_data = yf.download(stock_symbols, start=start_date, end=end_date)
        closing_prices = stock_data["Close"]

        # Calculate daily returns
        daily_returns = closing_prices.pct_change()

        # Calculate mean returns and covariance matrix
        mean_returns = daily_returns.mean()
        covariance_matrix = daily_returns.cov()

        return mean_returns, covariance_matrix
    except Exception as e:
        print(f"Error fetching stock data: {e}")
        return None, None
