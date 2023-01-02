import subprocess
import sys
import requests
import pytest
from requests.auth import HTTPBasicAuth
import random
import string

username = 'admin'
password = 'admin'
url_server = "http://localhost:8000/players?page="
base_url = 'http://localhost:8000/players?page=2'
logfile = "log.log"
cpu_threshold = 95
mem_threshold = 45
max_microseconds = 35000


@pytest.mark.usefixtures("start_server_and_log")
def test_warn_wrong_login(start_server_and_log):
    requests.get(base_url, auth=HTTPBasicAuth("username", "password"))
    requests.get(base_url, auth=HTTPBasicAuth("username", "password"))
    start_server_and_log.close()
    with open(logfile) as f:
        lines = f.readlines()
    for line in lines:
        assert f"{username}/{password}" not in line, print(f'{username} and {password} in the warn from server {line}')


class TestLogin:

    def test_login_correct(self, start_server):
        """login ok"""
        response = requests.get(base_url, auth=HTTPBasicAuth(username, password))
        assert response.status_code == 200, print(f"wrong status code, expected 200, actual {response.status_code}")

    def test_login_incorrect_password(self, start_server):
        """Server accepts client even that the password is incorrect"""
        response = requests.get(base_url,
                                auth=HTTPBasicAuth(username, password+"ll"))
        assert response.status_code == 401, print(f"wrong status code, expected 401 actual {response.status_code}")

    def test_login_incorrect_username(self, start_server):
        """Server accepts client even that the username is incorrect"""
        response = requests.get(base_url,
                                auth=HTTPBasicAuth("ll"+username, password))
        assert response.status_code == 401, print(f"wrong status code, expected 401 actual {response.status_code}")

    @pytest.mark.skip
    def test_vulnerability(self, start_server):
        """the server is vulnerability - Server doesn’t reject a client after a lot of wrong attempts"""
        for i in range(200000):
            # get random string of length 2 without repeating letters
            random_usr = ''.join(random.sample(string.ascii_lowercase, 5))
            random_pas = ''.join(random.sample(string.ascii_lowercase, 5))
            response = requests.get(base_url,
                                    auth=HTTPBasicAuth(random_usr, random_pas))
            assert response.status_code == 200, print(f"Server doesn't reject a client after a lot of wrong attempts.")

    def test_server_reject(self, start_server):
        """Server doesn’t reject a client after a lot of wrong attempts"""
        list_user_pass = "root", "administrator", "user", "try", "", "user2", "user3", "python", "player", "page"
        response = ""
        for name in list_user_pass:
            response = requests.get(base_url, auth=HTTPBasicAuth(name, name))
        assert response.status_code == 429


class TestInvalidPage:

    def test_zero_page(self, start_server):
        """The server returns status code 418, when the client tries to access zero page instead of status code 404"""
        response = requests.get(url_server + "0", auth=HTTPBasicAuth(username, password))
        assert response.status_code == 404, print("wrong status code")

    def test_char_page(self, start_server):
        """The server returns status code 418, when the client tries to access char page instead of status code 404"""
        response = requests.get(url_server + "s", auth=HTTPBasicAuth(username, password))
        assert response.status_code == 404, print("wrong status code")

    def test_negative_number_page(self, start_server):
        """The server returns status code 418,
        when the client tries to access negative number page instead of status code 404"""
        response = requests.get(url_server + "-6", auth=HTTPBasicAuth(username, password))
        assert response.status_code == 404, print("wrong status code")


class TestNotSupportedMethods:

    def test_delete(self, start_server):
        """The server returns status code 200 when the client tries to access delete methods"""
        response = requests.delete(base_url, auth=HTTPBasicAuth("username", username))
        assert response.status_code == 405, print(f"Status code return {response.status_code} instead of 406")

    def test_post(self, start_server):
        """The server returns status code 200 when the client tries to access post methods"""
        response = requests.post(base_url, auth=HTTPBasicAuth("username", username))
        assert response.status_code == 405, print(f"Status code return {response.status_code} instead of 406")

    def test_put(self, start_server):
        """The server returns status code 200 when the client tries to access put methods"""
        response = requests.put(base_url, auth=HTTPBasicAuth("username", username))
        assert response.status_code == 405, print(f"Status code return {response.status_code} instead of 406")

    def test_patch(self, start_server):
        """The server returns status code 200 when the client tries to access patch methods"""
        response = requests.patch(base_url, auth=HTTPBasicAuth("username", username))
        assert response.status_code == 405, print(f"Status code return {response.status_code} instead of 406")


class TestGetPlayer:
    def test_value_not_empty(self, start_server):
        """Test if name or id is empty"""
        response = requests.get(base_url, auth=HTTPBasicAuth("username", username))
        list_player = response.json()
        for dict_plyer in list_player:
            for k, v in dict_plyer.items():
                assert k and v, print(f"no value in {dict_plyer}")


class TestReliability:
    """get twice from server and compare the result is not changed"""
    def test_get_twice_from_server_and_compare(self, start_server):
        response = requests.get(base_url, auth=HTTPBasicAuth(username, password))
        list_player1 = response.json()
        response = requests.get(base_url, auth=HTTPBasicAuth(username, password))
        list_player2 = response.json()
        count_player = len(list_player1) if len(list_player2) > len(list_player1) else len(list_player2)
        for i in range(count_player):
            assert list_player1[i] == list_player2[i], \
                print(f"The data from the server is changed for each get first time: "
                      f"{list_player1[i]} second time: {list_player2[i]}")

    def test_id_of_player(self, start_server):
        """Each page is missing the last player"""
        pages = 3
        player_list_3_pages = []
        for i in range(pages):
            response = requests.get(url_server+str(i+1), auth=HTTPBasicAuth(username, password))
            player_list_3_pages.append(response.json())
        for i in range(pages-1):
            assert player_list_3_pages[i][-1]["ID"] + 1 == player_list_3_pages[i+1][0]["ID"],\
                print("Each page is missing the last player")

    def test_page_17_null(self, start_server):
        """tests page 17 is null"""
        response = requests.get(url_server + str(17), auth=HTTPBasicAuth(username, password))
        list_player = response.json()
        for dict_plyer in list_player:
            for k, v in dict_plyer.items():
                assert v != "null", print(f"no value in {dict_plyer}")

    def test_from_page_18(self,start_server):
        """From page 18, all the data is the same in every page"""
        pages = 3
        player_list_3_pages = []
        for i in range(18, 21):
            response = requests.get(url_server+str(i+1), auth=HTTPBasicAuth(username, password))
            player_list_3_pages.append(response.json())
        for i in range(pages-1):
            for j in range(len(player_list_3_pages[i])):
                assert player_list_3_pages[i][j]["ID"] != player_list_3_pages[i+1][j]["ID"]


class TestPerformance:
    def test_cpu(self, get_performance):
        """Test cpu"""
        assert max(get_performance["CPU"]) < cpu_threshold

    def test_memory(self, get_performance):
        """Test memory"""
        assert max(get_performance["MEMORY"]) < mem_threshold

    def test_time_response(self, get_performance):
        """Test the time of response"""
        assert max(get_performance["TIME_RES"]).microseconds < max_microseconds


@pytest.mark.skip
class TestParallel:

    def test_get_from_different_pages_parallel(self):
        p = subprocess.Popen(['pytest', 'test_get_from_different_pages.py', '--workers', '8'],
                             stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        res = p.communicate()
        assert b"FAILED" not in res[0]

    def test_get_from_the_same_pages_parallel(self):
        p = subprocess.Popen(['pytest', 'tests_get_from_the_same_page.py', '--workers', '8'],
                             stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        res = p.communicate()
        assert b"FAILED" not in res[0]


@pytest.mark.skip
class TestStress:
    def test_stress(self, start_server):
        for i in range(200000):
            response = requests.get(base_url,
                                    auth=HTTPBasicAuth(username, password))
            assert response.status_code == 200







