import plotly.graph_objects as go
import numpy as np


def plot_efficient_frontier(max_sharpe_ratio, min_volatility, efficient_list, target_returns):
    """
    Plots the efficient frontier along with maximum Sharpe ratio and minimum volatility points.

    Args:
        max_sharpe_ratio (tuple): Standard deviation and returns of the max Sharpe ratio portfolio.
        min_volatility (tuple): Standard deviation and returns of the min volatility portfolio.
        efficient_list (list): List of volatilities on the efficient frontier.
        target_returns (list): List of target returns corresponding to the efficient frontier.

    Returns:
        None
    """
    max_std, max_ret = max_sharpe_ratio
    min_std, min_ret = min_volatility

    # Plot Max Sharpe Ratio
    max_sharpe_trace = go.Scatter(
        name="Max Sharpe Ratio",
        mode="markers",
        x=[max_std * 100],
        y=[max_ret * 100],
        marker=dict(color="red", size=14, line=dict(width=3, color="black")),
    )

    # Plot Min Volatility
    min_vol_trace = go.Scatter(
        name="Min Volatility",
        mode="markers",
        x=[min_std * 100],
        y=[min_ret * 100],
        marker=dict(color="green", size=14, line=dict(width=3, color="black")),
    )

    # Plot Efficient Frontier
    efficient_frontier_trace = go.Scatter(
        name="Efficient Frontier",
        mode="lines",
        x=np.round(np.array(efficient_list) * 100, 2),
        y=np.round(np.array(target_returns) * 100, 2),
        line=dict(color="black", width=2, dash="solid"),
    )

    # Combine traces
    data = [max_sharpe_trace, min_vol_trace, efficient_frontier_trace]

    # Define layout
    layout = go.Layout(
        title="Portfolio Optimization with Efficient Frontier",
        yaxis=dict(title="Annualized Return (%)", tickformat=".2f"),
        xaxis=dict(title="Annualized Volatility (%)", tickformat=".2f"),
        showlegend=True,
        legend=dict(
            x=0.75, y=0, traceorder="normal", bgcolor="white", bordercolor="black", borderwidth=2
        ),
        width=800,
        height=600,
    )

    # Create and display the figure
    fig = go.Figure(data=data, layout=layout)
    fig.show()
