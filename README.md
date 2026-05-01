# Binance Futures Trading Bot

## Overview
A CLI-based Python trading bot that places Market and Limit orders on Binance Futures Testnet.

## Features
- Place MARKET and LIMIT orders
- Supports BUY and SELL
- CLI interface using argparse
- Logging of all API requests/responses
- Error handling and validation

## Setup

1. Clone repo:
git clone <your-repo-link>

2. Install dependencies:
pip install -r requirements.txt

3. Create .env file:
BINANCE_API_KEY=your_key
BINANCE_API_SECRET=your_secret

## Usage

Market Order:
python cli.py place --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001

Limit Order:
python cli.py place --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 90000

Check price:
python cli.py price --symbol BTCUSDT

Check account:
python cli.py account

## Logs
Logs are stored in logs/ folder with full API request/response details.

## Assumptions
- Uses Binance Futures Testnet
- LIMIT orders use GTC# binance-trading-bot
