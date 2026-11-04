import os

import requests

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")


def call(method, path, data=None):
    """Llama a la API. Devuelve (datos, error). Si todo va bien, error es None."""
    try:
        response = requests.request(method, API_URL + path, json=data, timeout=10)
    except requests.RequestException:
        return None, "API not available"

    body = response.json() if response.text else None
    if response.status_code >= 400:
        return None, body["error"]
    return body, None


def get_all(table):
    return call("GET", f"/{table}")


def get(table, item_id):
    return call("GET", f"/{table}/{item_id}")


def create(table, data):
    return call("POST", f"/{table}", data)


def update(table, item_id, data):
    return call("PUT", f"/{table}/{item_id}", data)


def delete(table, item_id):
    return call("DELETE", f"/{table}/{item_id}")
