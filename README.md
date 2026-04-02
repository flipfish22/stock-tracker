# 📈 Stock Tracker

A lightweight, interactive stock tracking app built with **Python**, **Streamlit**, and **Plotly**. Enter any ticker symbol(s) to view historical price charts, key metrics, and raw OHLCV data — all powered by Yahoo Finance via `yfinance`.

## Features

- 🔍 **Multi-ticker support** — track one or more stocks simultaneously
- 📊 **Line & Candlestick charts** — toggle between chart types with a click
- 📅 **Flexible time ranges** — 1 week up to 5 years
- 💡 **Key metrics** — current price, daily change, company name
- 📋 **Raw data table** — inspect the last 30 rows of OHLCV data
- ⚡ **5-minute caching** — minimizes redundant API calls

## Tech Stack

| Library | Purpose |
|---|---|
| `streamlit` | Web UI framework |
| `yfinance` | Yahoo Finance data fetcher |
| `pandas` | Data manipulation |
| `plotly` | Interactive charting |

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/flipfish22/stock-tracker.git
cd stock-tracker
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
streamlit run app.py
```

The app will open automatically at `http://localhost:8501`.

## Project Structure

```
stock-tracker/
├── app.py             # Main Streamlit application
├── requirements.txt   # Python dependencies
├── .gitignore         # Python + Streamlit ignores
└── README.md          # This file
```

## Roadmap

- [ ] Portfolio tracking (multiple tickers with weights)
- [ ] Price alerts / notifications
- [ ] Moving average overlays (SMA, EMA)
- [ ] Volume chart
- [ ] Export data to CSV
- [ ] Deploy to Streamlit Community Cloud

## License

MIT