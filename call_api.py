import requests
import sys
import json

# Use of the monitoring server API is subject to a query limit of 300 requests for a specific account token per day
# The monitoring server API allows up to 3 concurrent API calls from the same source IP.

BASE_URL = "https://monitoringapi.solaredge.com/site/{}/{}"


def fetch_detail_data_from_solaredge(site_id, api_key):
    endpoint = BASE_URL.format(site_id, "details")
    print("Calling endpoint: ", endpoint)
    response = requests.get(endpoint, params={"api_key": api_key})
    response.raise_for_status()
    return response.json()


def fetch_sites_data_from_solaredge(api_key):
    endpoint = "https://monitoringapi.solaredge.com//sites/list"
    print("Calling endpoint: ", endpoint)
    response = requests.get(endpoint, params={"api_key": api_key})
    response.raise_for_status()
    return response.json()


def fetch_overview_data_from_solaredge(site_id, api_key):
    endpoint = BASE_URL.format(site_id, "overview")
    print("Calling endpoint: ", endpoint)
    response = requests.get(endpoint, params={"api_key": api_key})
    response.raise_for_status()
    return response.json()


def fetch_alert_data_from_solaredge(site_id, api_key):
    endpoint = BASE_URL.format(site_id, "alerts")
    print("Calling endpoint: ", endpoint)
    response = requests.get(endpoint, params={"api_key": api_key})
    response.raise_for_status()
    return response.json()


def main():
    if len(sys.argv) > 1:
        site_id = sys.argv[1]
        api_key = sys.argv[2]
    else:
        site_id = input("Please enter your SolarEdge Site ID: ").strip()
        api_key = input("Please enter your SolarEdge API key: ").strip()

    try:
        data = fetch_detail_data_from_solaredge(site_id, api_key)
        print("Site Details:\n", json.dumps(data, indent=4))
    except requests.HTTPError as e:
        print(e.response.text)
        sys.exit(1)

    try:
        data = fetch_sites_data_from_solaredge(api_key)
        print("Sites List:\n", json.dumps(data, indent=4))
    except requests.HTTPError as e:
        print(e.response.text)
        sys.exit(1)

    try:
        data = fetch_overview_data_from_solaredge(site_id, api_key)
        print("Overview:\n", json.dumps(data, indent=4))
    except requests.HTTPError as e:
        print(e.response.text)
        sys.exit(1)


    try:
        data = fetch_alert_data_from_solaredge(site_id, api_key)
        print("Alerts:\n", json.dumps(data, indent=4))
    except requests.HTTPError as e:
        print(e.response.text)
        sys.exit(1)


if __name__ == "__main__":
    main()
