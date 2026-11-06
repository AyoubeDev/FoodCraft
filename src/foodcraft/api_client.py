import os

import requests

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")


def call(method, path, data=None):
    """Llama a la API. Devuelve (datos, error). Si todo va bien, error es None."""
    try:
        response = requests.request(method, API_URL + path, json=data, timeout=10)
    except requests.RequestException:
        return None, "API not available"
    
    # request(method). method es el metodo HTTP, por ejemplo "GET", POST, PUT, DELETE 
    # API_URL + path es la direcció de la API mes la ruta, per ejemplo, http://127:0.0.1:8000/users
    # json=data es que envia datos en cuerpo JSON, de su formato (serializacion)
    # timeout = 10 espera 10 segundos para la respuesta
    # En caso de que no se consiga comunicar con la API, ya sea en el tiempo establecido o por que este apagada, 
    # llama el except, y devuelve el (None, "Api not available")

    if response.text:
        body = response.json()
    else:
        body = None
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

#cada funcion es una orden diferente al servidor, 