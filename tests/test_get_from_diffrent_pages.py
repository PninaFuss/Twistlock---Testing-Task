import subprocess
import requests
import pytest
from requests.auth import HTTPBasicAuth

username = 'admin'
password = 'admin'
url_server = "http://localhost:8000/players?page="


@pytest.fixture(autouse=True, scope="function")
def start_server():
        p = subprocess.Popen("./twtask")
        yield
        print(p)


def test_get_one(start_server):
    response = requests.get(url_server+"1", auth=HTTPBasicAuth(username, password))
    assert response.status_code == 200


def test_get_two(start_server):
    response = requests.get(url_server+"2", auth=HTTPBasicAuth(username, password))
    assert response.status_code == 200


def test_get_three(start_server):
    response = requests.get(url_server+"3", auth=HTTPBasicAuth(username, password))
    assert response.status_code == 200


def test_get_four(start_server):
    response = requests.get(url_server+"4", auth=HTTPBasicAuth(username, password))
    assert response.status_code == 200


def test_get_five(start_server):
    response = requests.get(url_server+"5", auth=HTTPBasicAuth(username, password))
    assert response.status_code == 200


def test_get_six(start_server):
    response = requests.get(url_server+"6", auth=HTTPBasicAuth(username, password))
    assert response.status_code == 200


def test_get_seven(start_server):
    response = requests.get(url_server+"7", auth=HTTPBasicAuth(username, password))
    assert response.status_code == 200


def test_get_eight(start_server):
    response = requests.get(url_server+"8", auth=HTTPBasicAuth(username, password))
    assert response.status_code == 200


def test_get_nine(start_server):
    response = requests.get(url_server+"9", auth=HTTPBasicAuth(username, password))
    assert response.status_code == 200



