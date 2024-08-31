import pytest 
import requests

# URL_API = "127.0.0.1:5000/saludo/Seba"

def test_saludo_test():
    response = requests.get("http://localhost:5000/saludo/Seba")

    json_test = response.json()
    assert response.status_code == 200
    # assert isinstance(json_test['message'], list)

def test_saludo():
    response = requests.get("http://localhost:5000/saludo/Seba")

    json_test = response.json()
    # assert response.status_code == 200
    assert isinstance(json_test['message'], str)