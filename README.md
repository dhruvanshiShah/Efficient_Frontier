# Efficient Frontier Optimization

## Overview
The Efficient Frontier Optimization project is a Python-based application designed to analyze and optimize investment portfolios. It uses historical stock data to construct and analyze the efficient frontier, aiming to maximize the Sharpe Ratio and minimize volatility. This project utilizes various financial optimization techniques and provides visualizations of portfolio performance and the efficient frontier.

## Installation
### Clone the repo
```
git clone https://github.com/dhruvanshiShah/Efficient_FrontierMPT.git
cd efficient-frontier
```
### Install Dependencies
```
pip install -r requirements.txt
```
## Usage
### Configuration file
Create a YAML config file ```config.yaml``` with your parameters, or use command-line arguments:
```
stocks:
  - AMZN
  - AAPL
  - MSFT
  - GOOGL
  - TSLA
  - META
  - NVDA
  - NFLX
  - IBM

start_date: "2015-01-01"
end_date: "2024-01-01"
risk_free_rate: 0.01
```
### Command-Line Arguments
You can also pass parameters directly via command-line arguments:
```
python main.py --config config.yaml
```
## Repository Structure
```plaintext
Efficient_Frontier_MPT/
│
├── main.py
├── requirements.txt
├── config.yaml
├── README.md
├── utils/
  ├── __init__.py
  ├── data_processing.py
  ├── optimization.py
  └── visualization.py

