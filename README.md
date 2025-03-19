# Crypto Trading Bot - Binance & Telegram Integration

This is a Python-based crypto trading bot that integrates with Binance for executing trades and with Telegram for sending notifications. The bot performs buy and sell operations based on live market prices and implements a stop-loss mechanism to minimize potential losses. The bot utilizes the Binance API for real-time price feeds and the Telebot API for sending updates to a Telegram channel.

## Features

- **Real-Time Price Feeds**: Continuously fetches the latest prices for a specified trading pair (e.g., BTC/USDT) from Binance using WebSocket.
- **Buy/Sell Operations**: 
  - The bot can buy a cryptocurrency pair (e.g., BTC/USDT) with the available balance in USDT.
  - After buying, it can automatically sell when a price threshold (stop-loss) is hit.
- **Stop-Loss Mechanism**: Automatically triggers a sell order when the price of the asset drops below a certain percentage (stop-loss).
- **Telegram Notifications**: Sends buy/sell updates and profit information to a specified Telegram channel.
- **Customizable Fees and Stop-Loss**: You can define the fee percentage and stop-loss percentage as per your requirements.

## Requirements

- Python 3.7+
- `binance` (for interacting with Binance API)
- `pyTelegramBotAPI` (for interacting with Telegram API)

You can install the required dependencies using pip:

```bash
pip install python-binance pyTelegramBotAPI
