import subprocess
import requests
import pytest
from requests.auth import HTTPBasicAuth

username = 'admin'
password = 'admin'
base_url = 'http://localhost:8000/players?page=8'
logfile = "log_from_the_same_page.log"


@pytest.fixture(autouse=True, scope="function")
def start_server():
    outfile = open(logfile, 'w')
    p = subprocess.Popen("../twtask", bufsize=0, stdout=outfile)
    yield
    outfile.close()
    with open(logfile) as f:
        lines = f.readlines()
    print(lines)
    p.kill()


@pytest.mark.parametrize("number", [x for x in range(8)])
def test_get_one(start_server, number):
    response = requests.get(base_url, auth=HTTPBasicAuth(username, password))
    assert response.status_code == 200
