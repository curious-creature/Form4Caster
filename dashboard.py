import streamlit as st
import pandas as pd
import time

# Import the brain and the scraper you already built
from scrapers.sec_scraper import fetch_live_firehose
from analyzers.sentiment_engine import get_company_sentiment

# The Translation Bridge (Adding DUOT from your real test!)
TICKER_MAP = {
    "APPLE INC": "AAPL",
    "TESLA MOTORS INC": "TSLA",
    "TESLA, INC.": "TSLA",
    "MICROSOFT CORP": "MSFT",
    "AMAZON COM INC": "AMZN",
    "NVIDIA CORP": "NVDA",
    "META PLATFORMS INC": "META",
    "ALPHABET INC.": "GOOGL",
    "DUOS TECHNOLOGIES GROUP": "DUOT" 
}

# --- UI SETUP ---
# This configures the webpage title and makes it stretch across the screen
st.set_page_config(page_title="Form4Caster Terminal", layout="wide", page_icon="📈")

# The Header
st.title("📈 Form4Caster: Alternative Data Terminal")
st.markdown("Real-time monitoring of SEC Form 4 insider filings, cross-referenced with live NLP news sentiment.")
st.divider()

# --- THE SIDEBAR CONTROLS ---
st.sidebar.header("Terminal Controls")
st.sidebar.markdown("Click below to ping the SEC servers.")

# This button triggers the entire engine
if st.sidebar.button("Run Alpha Engine", type="primary"):
    
    # 1. INGESTION (With a loading spinner for the UI)
    with st.spinner("Tapping into SEC EDGAR live firehose..."):
        trades_list = fetch_live_firehose()
        
    if not trades_list:
        st.warning("No recent trades found on the SEC network. The market might be quiet. Try again in a minute.")
    else:
        df = pd.DataFrame(trades_list)
        st.success(f"Successfully captured {len(df)} live trades from the US Government.")
        
        # 2. PROCESSING & MAPPING
        df['Sentiment_Score'] = 0.0
        df['Ticker'] = "UNKNOWN"
        
        for index, row in df.iterrows():
            company_name = row['Company'].upper()
            for key in TICKER_MAP:
                if key in company_name:
                    df.at[index, 'Ticker'] = TICKER_MAP[key]
                    break
                    
        # 3. SENTIMENT INJECTION
        valid_trades = df[df['Ticker'] != "UNKNOWN"]
        
        if valid_trades.empty:
            st.info("No mapped companies traded recently. Displaying raw SEC feed instead:")
            # Display the raw dataframe cleanly
            st.dataframe(df[['Company', 'Insider', 'Time', 'Filing_URL']], use_container_width=True)
            
        else:
            with st.spinner("Running NLP Sentiment Engine on matched tickers..."):
                unique_tickers = valid_trades['Ticker'].unique()
                score_cache = {}
                
                for ticker in unique_tickers:
                    score_cache[ticker] = get_company_sentiment(ticker)
                    
                for index, row in df.iterrows():
                    ticker = row['Ticker']
                    if ticker in score_cache:
                        df.at[index, 'Sentiment_Score'] = score_cache[ticker]
                        
            final_report = df[df['Ticker'] != "UNKNOWN"]
            
            # --- FINAL UI DISPLAY ---
            
            # A. The Anomaly Alert System
            anomalies = final_report[final_report['Sentiment_Score'] <= -0.1]
            if not anomalies.empty:
                st.error("🚨 HIGH-VALUE ANOMALIES DETECTED 🚨")
                for _, row in anomalies.iterrows():
                    st.markdown(f"**Insider {row['Insider']}** just traded **{row['Ticker']}** despite NEGATIVE public sentiment ({row['Sentiment_Score']}).")
                    st.markdown(f"[🔗 View Official SEC Legal Document]({row['Filing_URL']})")
            
            # B. The Main Data Table
            st.subheader("Analyzed Trades")
            st.dataframe(
                final_report[['Ticker', 'Insider', 'Sentiment_Score', 'Time', 'Filing_URL']], 
                use_container_width=True
            )