
import sys
import google.auth
from google.auth.transport.requests import Request
from google.oauth2 import id_token
import requests

def verify_iap(url, audience):
    print(f"Target URL: {url}")
    print(f"Target Audience: {audience}")

    try:
        # Obtain ID token using ADC
        print("Gathering ADC credentials...")
        creds, project = google.auth.default()

        # We need to refresh the credentials to get the token, but for ID token we specifically use fetch_id_token
        # However, google.auth.default() returns credentials that might be user credentials or service account.
        # id_token.fetch_id_token is the helper for this.

        print("Fetching ID token...")
        request = Request()
        token = id_token.fetch_id_token(request, audience)

        print(f"Token obtained (len={len(token)}). Verifying with request...")

        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(url, headers=headers)

        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {response.headers}")
        print(f"Response Body Preview: {response.text[:200]}")

        if response.status_code == 200:
            print("SUCCESS: Connection verified.")
        elif response.status_code == 401:
            print("FAILURE: 401 Unauthorized. IAP likely rejected the token.")
        else:
            print(f"FAILURE: Unexpected status code {response.status_code}")

    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 verify_iap.py <url> <audience>")
        sys.exit(1)

    url = sys.argv[1]
    audience = sys.argv[2]
    verify_iap(url, audience)
