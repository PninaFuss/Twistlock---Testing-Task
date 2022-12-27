import subprocess
import requests
import pytest
from requests.auth import HTTPBasicAuth


logfile = "log.log"
username = 'admin'
password = 'admin'
base_url = 'http://localhost:8000/players?page=8'
number = 5


@pytest.fixture(autouse=True, scope="function")
def log_server():
    outfile = open(logfile, 'w')
    p = subprocess.Popen("./twtask", bufsize=0, stdout=outfile)
    yield outfile
    p.kill()


def test_worn_wrong_login(log_server):
    requests.get(base_url, auth=HTTPBasicAuth("username", "password"))
    log_server.close()
    with open(logfile) as f:
        lines = f.readlines()
    for line in lines:
        assert f"{username}/{password}" not in line , print(f'{username} and {password} in the warn from server {line}')




