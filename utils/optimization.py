import numpy as np
from scipy.optimize import minimize


def calculate_portfolio_performance(portfolio_weights, mean_returns, covariance_matrix):
    """
    Calculates the annualized portfolio performance given weights, mean returns, and covariance matrix.

    Args:
        portfolio_weights (numpy.ndarray): Array of portfolio weights.
        mean_returns (pandas.Series): Mean returns of the stocks.
        covariance_matrix (pandas.DataFrame): Covariance matrix of the stocks.

    Returns:
        tuple: Annualized standard deviation and annualized returns of the portfolio.
    """
    annual_returns = np.sum(mean_returns * portfolio_weights) * 252
    annual_std_dev = np.sqrt(
        np.dot(portfolio_weights.T, np.dot(covariance_matrix, portfolio_weights))
    ) * np.sqrt(252)
    return annual_std_dev, annual_returns


def negative_sharpe_ratio(portfolio_weights, mean_returns, covariance_matrix, risk_free_rate=0):
    """
    Calculates the negative Sharpe ratio for optimization purposes.

    Args:
        portfolio_weights (numpy.ndarray): Array of portfolio weights.
        mean_returns (pandas.Series): Mean returns of the stocks.
        covariance_matrix (pandas.DataFrame): Covariance matrix of the stocks.
        risk_free_rate (float): Risk-free rate of return.

    Returns:
        float: Negative Sharpe ratio.
    """
    portfolio_std_dev, portfolio_returns = calculate_portfolio_performance(
        portfolio_weights, mean_returns, covariance_matrix
    )
    sharpe_ratio = (portfolio_returns - risk_free_rate) / portfolio_std_dev
    return -sharpe_ratio


def maximize_sharpe_ratio(mean_returns, covariance_matrix, risk_free_rate=0, constraint_set=(0, 1)):
    """
    Maximizes the Sharpe ratio by optimizing portfolio weights.

    Args:
        mean_returns (pandas.Series): Mean returns of the stocks.
        covariance_matrix (pandas.DataFrame): Covariance matrix of the stocks.
        risk_free_rate (float): Risk-free rate of return.
        constraint_set (tuple): Bounds for each asset's allocation in the portfolio.

    Returns:
        OptimizeResult: Optimization result containing portfolio weights and performance metrics.
    """
    num_assets = len(mean_returns)
    args = (mean_returns, covariance_matrix, risk_free_rate)
    constraints = {"type": "eq", "fun": lambda x: np.sum(x) - 1}
    bounds = tuple(constraint_set for _ in range(num_assets))
    result = minimize(
        negative_sharpe_ratio,
        num_assets * [1.0 / num_assets],
        args=args,
        method="SLSQP",
        bounds=bounds,
        constraints=constraints,
    )
    if not result.success:
        print("Warning: Optimization did not converge")
    return result


def minimize_volatility(mean_returns, covariance_matrix, constraint_set=(0, 1)):
    """
    Minimizes the portfolio volatility by optimizing portfolio weights.

    Args:
        mean_returns (pandas.Series): Mean returns of the stocks.
        covariance_matrix (pandas.DataFrame): Covariance matrix of the stocks.
        constraint_set (tuple): Bounds for each asset's allocation in the portfolio.

    Returns:
        OptimizeResult: Optimization result containing portfolio weights and performance metrics.
    """
    num_assets = len(mean_returns)
    constraints = {"type": "eq", "fun": lambda x: np.sum(x) - 1}
    bounds = tuple(constraint_set for _ in range(num_assets))
    result = minimize(
        lambda x: calculate_portfolio_performance(x, mean_returns, covariance_matrix)[0],
        num_assets * [1.0 / num_assets],
        method="SLSQP",
        bounds=bounds,
        constraints=constraints,
    )
    if not result.success:
        print("Warning: Optimization did not converge")
    return result


def efficient_optimization(mean_returns, covariance_matrix, return_target, constraint_set=(0, 1)):
    """
    Finds the portfolio with minimum volatility for a given target return.

    Args:
        mean_returns (pandas.Series): Mean returns of the stocks.
        covariance_matrix (pandas.DataFrame): Covariance matrix of the stocks.
        return_target (float): Target return for the efficient frontier.
        constraint_set (tuple): Bounds for each asset's allocation in the portfolio.

    Returns:
        OptimizeResult: Optimization result containing portfolio weights and performance metrics.
    """
    num_assets = len(mean_returns)
    constraints = (
        {
            "type": "eq",
            "fun": lambda x: calculate_portfolio_performance(x, mean_returns, covariance_matrix)[1]
            - return_target,
        },
        {"type": "eq", "fun": lambda x: np.sum(x) - 1},
    )
    bounds = tuple(constraint_set for _ in range(num_assets))
    result = minimize(
        lambda x: calculate_portfolio_performance(x, mean_returns, covariance_matrix)[0],
        num_assets * [1.0 / num_assets],
        method="SLSQP",
        bounds=bounds,
        constraints=constraints,
    )
    if not result.success:
        print(f"Warning: Optimization did not converge for target return {return_target}")
    return result