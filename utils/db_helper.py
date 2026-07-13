import requests
import json
import logging

# Firebase REST API Base URL
BASE_URL = "https://sevgiliwepsite-default-rtdb.europe-west1.firebasedatabase.app"

def get_data(path):
    """Fetches data from Firebase at the given path."""
    try:
        url = f"{BASE_URL}/{path}.json"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logging.error(f"Error fetching data from {path}: {e}")
        return None

def put_data(path, data):
    """Writes/Overwrites data to Firebase at the given path."""
    try:
        url = f"{BASE_URL}/{path}.json"
        response = requests.put(url, json=data)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logging.error(f"Error putting data to {path}: {e}")
        return None

def patch_data(path, data):
    """Updates specific keys at the given path without overwriting everything."""
    try:
        url = f"{BASE_URL}/{path}.json"
        response = requests.patch(url, json=data)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logging.error(f"Error patching data to {path}: {e}")
        return None

def post_data(path, data):
    """Appends data to a list in Firebase (creates a unique ID key)."""
    try:
        url = f"{BASE_URL}/{path}.json"
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logging.error(f"Error posting data to {path}: {e}")
        return None

def delete_data(path):
    """Deletes data at the given path."""
    try:
        url = f"{BASE_URL}/{path}.json"
        response = requests.delete(url)
        response.raise_for_status()
        return True
    except Exception as e:
        logging.error(f"Error deleting data from {path}: {e}")
        return False
