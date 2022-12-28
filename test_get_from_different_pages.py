import subprocess
import requests
import pytest
from requests.auth import HTTPBasicAuth

username = 'admin'
password = 'admin'
url_server = "http://localhost:8000/players?page="
logfile = "log_from_different_pages.log"


@pytest.fixture(autouse=True, scope="function")
def start_server():
    outfile = open(logfile, 'w')
    p = subprocess.Popen("./twtask", bufsize=0, stdout=outfile)
    yield
    outfile.close()
    with open(logfile) as f:
        lines = f.readlines()
    print(lines)
    p.kill()


@pytest.mark.parametrize("page_number", [x+1 for x in range(8)])
def test_get_one(start_server, page_number):
    response = requests.get(url_server+str(page_number), auth=HTTPBasicAuth(username, password))
    assert response.status_code == 200




