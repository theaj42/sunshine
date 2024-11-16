import requests
from dotenv import load_dotenv
import os

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

def main():
    load_dotenv()
    api_key = os.getenv("CONGRESS_GOV_APIKEY")
    if not api_key:
        raise ValueError("No API key found. Please set the CONGRESS_GOV_APIKEY environment variable.")
    data = fetch_legislation(api_key)
    print(data)

if __name__ == "__main__":
    main()