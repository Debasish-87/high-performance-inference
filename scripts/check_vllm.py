
import requests
import sys
import os

BASE_URL = os.getenv(
    "VLLM_BASE_URL",
    "http://127.0.0.1:8000"
)

def main():
    url = f"{BASE_URL.rstrip('/')}/v1/models"

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()

        data = response.json()

        print("STATUS: vLLM RUNNING")
        print("HTTP:", response.status_code)

        for model in data.get("data", []):
            print("Model:", model.get("id"))

    except requests.RequestException as exc:
        print("STATUS: vLLM NOT AVAILABLE")
        print("Error:", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()
