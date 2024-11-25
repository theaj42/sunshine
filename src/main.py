import requests
from dotenv import load_dotenv
import os
import json
from datetime import datetime
import ollama

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

def summarize_with_ollama(json_data):
    client = ollama.Client(host="http://10.10.10.220:11434")
    prompt = f"Summarize the following legislative bill details. Make sure your response is in well-formed markdown. {json.dumps(json_data)}"
    response = client.generate(model="llama3.2:latest", prompt=prompt)
    
    # Get response text and clean it
    text = response['response']
    
    # Remove surrounding quotes if present
    text = text.strip('"')
    
    # Replace escaped newlines with actual newlines
    text = text.encode().decode('unicode_escape')
    
    return text



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
    
    # Summarize the JSON file
    summary = summarize_with_ollama(bill_details)
    summary_filename = f"data/{date_str}_{bill_id}_summary.md"
    
    # Save the summary to a JSON file
    with open(summary_filename, 'w') as f:
        json.dump(summary, f, indent=4)
    
    print(f"Saved summary to {summary_filename}")

if __name__ == "__main__":
    main()