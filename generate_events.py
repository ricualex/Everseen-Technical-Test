import random
import uuid
import json
import requests


url = "http://127.0.0.1:8000/api/v1/data"
statuses = ["complete", "incomplete", "cancelled"]
types = [1, 2, 5, 11]

def generate_md5_hash():
    """Generate MD5 hash."""
    return uuid.uuid4().hex[:32]

def generate_valid_payload():
    """Generate a valid payload with random values."""
    payload = {
        "status": random.choice(statuses),
        "type": random.choice(types),
        "hash": generate_md5_hash()
    }
    return payload

def main():
    """
    Following script should call eReceiver endpoint with valid payloads, then the eReceiver will publish a Cloud Event Object 
    for each one of the requests, resulting in 100 Cloud Event objects.
    """
    num_events = 100
    for _ in range(num_events):
        payload = generate_valid_payload()
        try:
            response = requests.post(url, json=payload)
        except requests.exceptions.RequestException as e:
            print(f"Failed test with exception: {e}")
if __name__ == "__main__":
    main()