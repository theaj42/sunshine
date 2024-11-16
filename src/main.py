import requests
from dotenv import load_dotenv
import os
import json
from datetime import datetime

def fetch_legislation(api_key):
    url = "https://api.congress.gov/v3/bill"
    headers = {
        "X-API-Key": api_key
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def fetch_bill_details(api_key, bill_url):
    headers = {
        "X-API-Key": api_key
    }
    response = requests.get(bill_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def main():
    load_dotenv()
    api_key = os.getenv("CONGRESS_GOV_APIKEY")
    if not api_key:
        raise ValueError("No API key found. Please set the CONGRESS_GOV_APIKEY environment variable.")
    
    data = fetch_legislation(api_key)
    bills = data.get('bills', [])
    
    if not bills:
        print("No bills found.")
        return
    
    # Find the newest bill
    newest_bill = max(bills, key=lambda bill: bill['updateDate'])
    bill_details = fetch_bill_details(api_key, newest_bill['url'])
    
    # Create filename
    date_str = datetime.strptime(newest_bill['updateDate'], '%Y-%m-%d').strftime('%Y%m%d')
    bill_id = f"{newest_bill['type']}-{newest_bill['number']}"
    filename = f"data/{date_str}_{bill_id}.json"
    
    # Save to JSON file
    with open(filename, 'w') as f:
        json.dump(bill_details, f, indent=4)
    
    print(f"Saved bill details to {filename}")

if __name__ == "__main__":
    main()