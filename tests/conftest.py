import time

import pytest
import subprocess
import sys
import datetime
import psutil
import requests
from requests.auth import HTTPBasicAuth


logfile = "log.log"
username = 'admin'
password = 'admin'
url_server = "http://localhost:8000/players?page="
base_url = 'http://localhost:8000/players?page=2'


@pytest.fixture(autouse=False, scope="class")
def start_server():
    try:
        p = subprocess.Popen("./twtask")
        yield
        p.kill()
    except Exception as e:
        sys.exit(f"Error {e}")


@pytest.fixture(scope="function")
def start_server_and_log():
    try:
        outfile = open(logfile, 'w')
        p = subprocess.Popen("./twtask", bufsize=0, stdout=outfile)
        time.sleep(0.5)
        yield outfile
        p.kill()
    except Exception as e:
        sys.exit(f"Error {e}")


@pytest.fixture(autouse=False, scope="class")
def get_performance(start_server):
    time_response = []
    cpu_list = []
    mem_list = []
    for i in range(500):
        time_before = datetime.datetime.now()
        requests.get(base_url, auth=HTTPBasicAuth(username, password))
        time_after = datetime.datetime.now()
        time_response.append(time_after - time_before)
        cpu_list.append(psutil.cpu_percent())
        mem_list.append(psutil.virtual_memory().percent)
    return {"CPU": cpu_list, "MEMORY": mem_list, "TIME_RES": time_response}