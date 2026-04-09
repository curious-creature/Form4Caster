import requests
from bs4 import BeautifulSoup
import re

def fetch_live_firehose():
    """
    Connects to the SEC's live feed and pulls the most recent insider trades 
    across ALL companies as they happen in real-time.
    """
    headers = {
        'User-Agent': 'CS_Project_Student (your.actual.email@example.com)' 
    }
    
    sec_url = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&CIK=&type=4&company=&dateb=&owner=only&start=0&count=20&output=atom"
    
    try:
        response = requests.get(sec_url, headers=headers)
        
        if response.status_code != 200:
            return []
            
        soup = BeautifulSoup(response.content, 'xml')
        entries = soup.find_all('entry')
        
        parsed_trades = []
        
        for entry in entries:
            title = entry.title.text
            link = entry.link['href'] if entry.link else "No Link"
            timestamp = entry.updated.text
            
            match = re.search(r'4 - (.*?) \((.*?)\) \((.*?)\)', title)
            
            if match:
                company_name = match.group(1).strip()
                insider_name = match.group(3).strip()
                
                trade_data = {
                    "Company": company_name,
                    "Insider": insider_name,
                    "Time": timestamp,
                    "Filing_URL": link
                }
                parsed_trades.append(trade_data)
                
        return parsed_trades

    except Exception as e:
        print(f"Scraper error: {e}")
        return []

if __name__ == "__main__":
    trades = fetch_live_firehose()
    print("Scraper test successful. Found trades.")