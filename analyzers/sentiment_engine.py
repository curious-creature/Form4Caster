import yfinance as yf
from textblob import TextBlob

def get_company_sentiment(ticker):
    """
    Fetches recent news for a given stock ticker and calculates an average 
    sentiment score from -1.0 (Very Negative) to +1.0 (Very Positive).
    """
    print(f"Fetching latest news for {ticker.upper()}...")
    
    # 1. THE SETUP (Module IV - OOP & Objects)
    # We create a Ticker object using yfinance to interact with that specific stock
    stock = yf.Ticker(ticker)
    
    # 2. THE EXECUTION (Module IV - Exception Handling)
    try:
        # yfinance returns a list of dictionaries containing recent news articles
        news_articles = stock.news 
        
        if not news_articles:
            print(f"No recent news found for {ticker.upper()}.")
            return 0.0 # Return neutral if no news exists
            
        total_score = 0
        valid_articles = 0
        
        print("\n--- ANALYZING HEADLINES ---")
        
        # 3. THE ANALYSIS (Module III - Looping & Data Processing)
        for article in news_articles:
            title = article.get('title', '')
            
            if title:
                # TextBlob does the heavy lifting of reading the text.
                # .sentiment.polarity returns a float between -1.0 and 1.0.
                analysis = TextBlob(title)
                score = analysis.sentiment.polarity
                
                total_score += score
                valid_articles += 1
                
                # Print the headline and its individual score so we can see it working
                print(f"Score: {score:.2f} | Headline: {title}")
                
        # Calculate the average sentiment across all recent articles
        if valid_articles > 0:
            average_sentiment = total_score / valid_articles
            return round(average_sentiment, 3)
        else:
            return 0.0

    except Exception as e:
        print(f"An error occurred while fetching news: {e}")
        return 0.0

# 4. THE TEST RUN
if __name__ == "__main__":
    # Let's test it with a company that usually has a lot of news, like Tesla
    test_ticker = "TSLA"
    
    final_score = get_company_sentiment(test_ticker)
    
    print("\n--- FINAL VERDICT ---")
    print(f"Average Sentiment Score for {test_ticker}: {final_score}")
    
    if final_score > 0.1:
        print("Status: POSITIVE NEWS CYCLE")
    elif final_score < -0.1:
        print("Status: NEGATIVE NEWS CYCLE")
    else:
        print("Status: NEUTRAL")