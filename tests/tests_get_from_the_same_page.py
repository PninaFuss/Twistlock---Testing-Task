import subprocess
import requests
import pytest
from requests.auth import HTTPBasicAuth

username = 'admin'
password = 'admin'
base_url = 'http://localhost:8000/players?page=8'
number = 2


@pytest.fixture(autouse=True, scope="session")
def start_server():
        p = subprocess.Popen("./twtask")
        yield
        print(p)


def test_get_one(start_server):
    for i in range(number):
        response = requests.get(base_url, auth=HTTPBasicAuth(username, password))
        assert response.status_code == 200


def test_get_two(start_server):
    for i in range(number):
        response = requests.get(base_url, auth=HTTPBasicAuth(username, password))
        assert response.status_code == 200


def test_get_three(start_server):
    for i in range(number):
        response = requests.get(base_url, auth=HTTPBasicAuth(username, password))
        assert response.status_code == 200


def test_get_four(start_server):
    for i in range(number):
        response = requests.get(base_url, auth=HTTPBasicAuth(username, password))
        assert response.status_code == 200


def test_get_five(start_server):
    for i in range(number):
        response = requests.get(base_url, auth=HTTPBasicAuth(username, password))
        assert response.status_code == 200


def test_get_six(start_server):
    for i in range(number):
        response = requests.get(base_url, auth=HTTPBasicAuth(username, password))
        assert response.status_code == 200


def test_get_seven(start_server):
    for i in range(number):
        response = requests.get(base_url, auth=HTTPBasicAuth(username, password))
        assert response.status_code == 200


def test_get_eight(start_server):
    for i in range(number):
        response = requests.get(base_url, auth=HTTPBasicAuth(username, password))
        assert response.status_code == 200


def test_get_nine(start_server):
    for i in range(number):
        response = requests.get(base_url, auth=HTTPBasicAuth(username, password))
        assert response.status_code == 200






#
