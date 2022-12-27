import subprocess
import time

import requests
import pytest
from requests.auth import HTTPBasicAuth
import psutil

username = 'admin'
password = 'admin'
base_url = 'http://localhost:8000/players?page=8'
number = 20


@pytest.fixture(autouse=True, scope="session")
def start_server():
        p = subprocess.Popen("./twtask")
        yield
        print(p)


def test_get(start_server):
    for i in range(number):
        response = requests.get(base_url, auth=HTTPBasicAuth(username, password))
        assert response.status_code == 200


def test_get_cpu(start_server):
        # Calling psutil.cpu_precent() for 10 seconds
        assert psutil.cpu_percent(4) < 30


def test_get_men(start_server):
    for id in psutil.pids():
        p = psutil.Process(id)
        if p.name() == 'twtask':
            memory = p.memory_percent()
            cpu = p.cpu_percent()
            print("Memory Perentage for twtask process is " + str(memory))
            assert memory < 10
            assert cpu < 25

