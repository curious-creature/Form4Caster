# Form4Caster 📈

**Real-time SEC insider trading tracker cross-referenced with live NLP sentiment analysis.**

Form4Caster is a lightweight, alternative data context engine built in Python. It monitors the SEC's live EDGAR firehose for Form 4 filings (legal insider trades) and instantly correlates those trades with current public news sentiment to identify high-value market anomalies.

## 🧠 The Concept (Signal vs. Noise)
Retail investors usually hear about massive insider trades days after they happen. Institutional quant funds use algorithms to scrape this data in milliseconds. 

Form4Caster levels the playing field by not just aggregating the data, but analyzing the context:
* **The Normal:** A CEO buys $1M of stock during a positive news cycle. (Expected).
* **The Anomaly:** A CEO buys $1M of stock during an overwhelmingly *negative* news cycle. The public is panicking, but the insider is buying. (High-Value Signal).

## 🛠️ Tech Stack
* **Language:** Python 3.9+
* **Data Ingestion:** `requests`, `BeautifulSoup4`, `lxml` (SEC EDGAR scraping)
* **Financial Data & News:** `yfinance`
* **Natural Language Processing:** `TextBlob`
* **Data Manipulation:** `pandas`
* **Frontend Dashboard:** `streamlit`

## ✨ Features
* **Live SEC Firehose Integration:** Bypasses manual search and pulls live Form 4 XML data directly from the US Government.
* **Dynamic Ticker Mapping:** Automatically caches and maps SEC corporate legal names to their standard Yahoo Finance tickers using the master SEC JSON dictionary.
* **Automated Sentiment Scoring:** Scrapes recent headlines for mapped tickers and assigns a mathematical sentiment score (-1.0 to +1.0).
* **Anomaly Detection Alerts:** Automatically flags trades that occur against the grain of public sentiment.
* **Local Web Interface:** Clean, interactive Streamlit UI to view trades and follow direct links to official SEC legal documents.
