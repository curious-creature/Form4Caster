import pandas as pd
import time

# 1. IMPORTS: Bring in the modules we built in Step 1 and Step 2
from scrapers.sec_scraper import fetch_live_firehose
from analyzers.sentiment_engine import get_company_sentiment

# 2. DATA NORMALIZATION (Module III - Dictionaries)
# A simple mapper to translate SEC company names to Yahoo Finance tickers.
# In a massive hedge fund, this would be a database of 10,000+ companies.
TICKER_MAP = {
    "APPLE INC": "AAPL",
    "TESLA MOTORS INC": "TSLA",
    "TESLA, INC.": "TSLA",
    "MICROSOFT CORP": "MSFT",
    "AMAZON COM INC": "AMZN",
    "NVIDIA CORP": "NVDA",
    "META PLATFORMS INC": "META",
    "ALPHABET INC.": "GOOGL"
}

def run_alpha_engine():
    """
    The central nervous system of Form4Caster. 
    Pulls live trades, matches them to tickers, and calculates the sentiment alpha.
    """
    print("========================================")
    print("  INITIALIZING FORM4CASTER ENGINE")
    print("========================================\n")
    
    # --- PHASE 1: INGESTION ---
    trades_list = fetch_live_firehose()
    
    if not trades_list:
        print("No new trades found on the SEC network. Sleeping...")
        return

    # Convert our list of dictionaries into a Pandas DataFrame.
    # Think of a DataFrame as a highly programmable Excel spreadsheet inside Python.
    df = pd.DataFrame(trades_list)
    print(f"Captured {len(df)} live trades. Processing...\n")
    
    # --- PHASE 2: PROCESSING & MAPPING ---
    # We create a new empty column for our Sentiment Scores
    df['Sentiment_Score'] = 0.0
    df['Ticker'] = "UNKNOWN"
    
    # Loop through every row in our dataframe
    for index, row in df.iterrows():
        company_name = row['Company'].upper()
        
        # Check if the SEC company name exists in our dictionary
        # We use a partial match just in case the SEC adds weird characters
        for key in TICKER_MAP:
            if key in company_name:
                df.at[index, 'Ticker'] = TICKER_MAP[key]
                break
                
    # --- PHASE 3: THE NLP SENTIMENT INJECTION ---
    # We only want to run sentiment analysis on companies we have tickers for,
    # otherwise we waste time and bandwidth.
    valid_trades = df[df['Ticker'] != "UNKNOWN"]
    
    print("--- RUNNING SENTIMENT ANALYSIS ---")
    unique_tickers = valid_trades['Ticker'].unique()
    
    # Create a temporary dictionary to store scores so we don't look up the same company twice
    score_cache = {} 
    
    for ticker in unique_tickers:
        score = get_company_sentiment(ticker)
        score_cache[ticker] = score
        
    # Map the calculated scores back to our main DataFrame
    for index, row in df.iterrows():
        ticker = row['Ticker']
        if ticker in score_cache:
            df.at[index, 'Sentiment_Score'] = score_cache[ticker]

    # --- PHASE 4: THE OUTPUT ALGORITHM ---
    print("\n========================================")
    print("  FINAL ALPHA REPORT")
    print("========================================")
    
    # Filter the DataFrame to only show the trades we successfully analyzed
    final_report = df[df['Ticker'] != "UNKNOWN"]
    
    if final_report.empty:
        print("No major tech companies traded in the last 5 minutes.")
        print("Here is the raw SEC data instead:")
        print(df[['Company', 'Insider', 'Time']].head())
    else:
        # Print a clean, formatted table for the user
        print(final_report[['Ticker', 'Insider', 'Sentiment_Score', 'Time']])
        
        # Identify the High-Value Anomaly
        for index, row in final_report.iterrows():
            if row['Sentiment_Score'] <= -0.1:
                print(f"\nHIGH-VALUE ANOMALY DETECTED")
                print(f"Insider {row['Insider']} just traded {row['Ticker']} despite NEGATIVE public sentiment ({row['Sentiment_Score']}).")
                print(f"Investigate immediately: {row['Filing_URL']}")

if __name__ == "__main__":
    run_alpha_engine()