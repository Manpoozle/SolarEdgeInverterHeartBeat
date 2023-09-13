import requests
import sys
import json
from datetime import datetime
import time

RETRIES = 2
DELAY = 60  # seconds

BASE_URL = "https://monitoringapi.solaredge.com/site/{}/{}"
SITES_URL = "https://monitoringapi.solaredge.com/sites/list"


def fetch_data_from_solaredge(url, api_key):
    print("Calling endpoint: ", url)
    response = requests.get(url, params={"api_key": api_key})
    response.raise_for_status()
    return response.json()


def check_data_period_end_date(data_period):
    # Extract the endDate from the dataPeriod
    end_date_str = data_period.get('dataPeriod', {}).get('endDate', '')

    # Get today's date in the same format
    today_str = datetime.today().strftime('%Y-%m-%d')

    # Compare and return the result
    if end_date_str == today_str:
        return 0
    else:
        error_message = f"Error: The endDate {end_date_str} does not match today's date {today_str}."
        print(error_message)
        return 1


def main():
    if len(sys.argv) > 1:
        site_id = sys.argv[1]
        api_key = sys.argv[2]
    else:
        site_id = input("Please enter your SolarEdge Site ID: ").strip()
        api_key = input("Please enter your SolarEdge API key: ").strip()

    endpoints = {
        # "Site Details": BASE_URL.format(site_id, "details"),
        # "Sites List": SITES_URL,
        # "Overview": BASE_URL.format(site_id, "overview"),
        "Data Period": BASE_URL.format(site_id, "dataPeriod"),
        # "Alerts": BASE_URL.format(site_id, "alerts")
    }

    for description, url in endpoints.items():
        retries_left = RETRIES
        while retries_left > 0:
            try:
                data = fetch_data_from_solaredge(url, api_key)
                print(f"{description}:\n", json.dumps(data, indent=4))
                break  # If successful, break out of the retry loop
            except requests.HTTPError as e:
                print(f"Error fetching {description}. Retries left: {retries_left}")
                print(e.response.text)
                retries_left -= 1
                if retries_left > 0:  # Only sleep if there are retries left
                    time.sleep(DELAY)
        else:  # This will execute if the while loop exhausted all retries without a break
            print(f"Failed to fetch {description} after {RETRIES} retries.")
            sys.exit(1)

        result = check_data_period_end_date(data)
        sys.exit(result)


if __name__ == "__main__":
    main()
