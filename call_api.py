import requests
import sys

BASE_URL = "https://monitoringapi.solaredge.com/site/{}/details"


def fetch_data_from_solaredge(site_id, api_key):
    endpoint = BASE_URL.format(site_id)
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
        data = fetch_data_from_solaredge(site_id, api_key)
        print(data)
    except requests.HTTPError as e:
        print(e.response.text)
        sys.exit(1)


if __name__ == "__main__":
    main()
