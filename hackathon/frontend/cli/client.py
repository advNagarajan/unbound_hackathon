# cli/client.py

import requests
from cli.config import load_api_key

BASE_URL = "http://localhost:8000"   # change in deployment


def get_headers():
    api_key = load_api_key()
    if not api_key:
        raise Exception("You must login first using: gateway login <API_KEY>")
    return {
        "Authorization": f"ApiKey {api_key}",
        "Content-Type": "application/json"
    }


def get(path: str):
    return requests.get(BASE_URL + path, headers=get_headers())


def post(path: str, json=None):
    return requests.post(BASE_URL + path, json=json, headers=get_headers())


def delete(path: str):
    return requests.delete(BASE_URL + path, headers=get_headers())
