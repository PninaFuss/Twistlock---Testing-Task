import subprocess
import requests
import pytest
from requests.auth import HTTPBasicAuth
import random
import string

username = 'admin'
password = 'admin'
url_server = "http://localhost:8000/players?page="
base_url = 'http://localhost:8000/players?page=2'


@pytest.fixture(autouse=True, scope="session")
def start_server():
    p = subprocess.Popen("./twtask")
    yield
    p.kill()


class TestLogin:

    def test_login_correct(self, start_server):
        response = requests.get(base_url, auth=HTTPBasicAuth(username, password))
        assert response.status_code == 200, print(f"wrong status code, expected 200, actual {response.status_code}")

    def test_login_incorrect_password(self, start_server):
        response = requests.get(base_url,
                                auth=HTTPBasicAuth(username, password+"ll"))
        assert response.status_code == 401, print(f"wrong status code, expected 401 actual {response.status_code}")

    def test_login_incorrect_username(self, start_server):
        response = requests.get(base_url,
                                auth=HTTPBasicAuth("ll"+username, password))
        assert response.status_code == 401, print(f"wrong status code, expected 401 actual {response.status_code}")

    def test_login_incorrect_username_and_password(self, start_server):
        response = requests.get(base_url,
                                auth=HTTPBasicAuth(username+"kk", password+"uu"))
        assert response.status_code == 401, print(f"wrong status code, expected 401 actual {response.status_code}")


    def test_random_user(self,start_server):
        for i in range(500):
            # get random string of length 2 without repeating letters
            random_usr = ''.join(random.sample(string.ascii_lowercase, 2))
            random_pas = ''.join(random.sample(string.ascii_lowercase, 2))
            response = requests.get(base_url,
                                    auth=HTTPBasicAuth("adm" + random_usr, random_pas + "min"))
            assert response.status_code == 401, print(f"Server doesn't reject a client after a lot of wrong attempts.")


class TestInvalidPage:

    def test_zero_page(self, start_server):
        response = requests.get(url_server + "0", auth=HTTPBasicAuth(username, password))
        assert  response.status_code == 404, print("wrong status code")

    def test_char_page(self, start_server):
        response = requests.get(url_server + "s", auth=HTTPBasicAuth(username, password))
        assert  response.status_code == 404, print("wrong status code")

    def test_negative_number_page(self,start_server):
        response = requests.get(url_server + "-6", auth=HTTPBasicAuth(username, password))
        assert  response.status_code == 404, print("wrong status code")


class TestNotSupportedMethods:

    def test_delete(self, start_server):
        response = requests.delete(base_url, auth=HTTPBasicAuth("username", username))
        assert response.status_code == 406, print(f"Status code return {response.status_code} instead of 406")

    def test_post(self, start_server):
        response = requests.post(base_url, auth=HTTPBasicAuth("username", username))
        assert response.status_code == 406, print(f"Status code return {response.status_code} instead of 406")

    def test_put(self, start_server):
        response = requests.put(base_url, auth=HTTPBasicAuth("username", username))
        assert response.status_code == 406, print(f"Status code return {response.status_code} instead of 406")

    def test_patch(self, start_server):
        response = requests.patch(base_url, auth=HTTPBasicAuth("username", username))
        assert response.status_code == 406,print(f"Status code return {response.status_code} instead of 406")


class TestGetPlayer:
    def test_get_player(self, start_server):
        response = requests.get(base_url, auth=HTTPBasicAuth("username", username))
        list_player = response.json()
        for dict_plyer in list_player:
            for k, v in dict_plyer.items():
                assert k and v, print(f"no value in {dict_plyer}")


class TestRelability:
    def test_get_twice_from_server_and_compare(self,start_server):
        response = requests.get(base_url, auth=HTTPBasicAuth(username, password))
        list_player1 = response.json()
        response = requests.get(base_url, auth=HTTPBasicAuth(username, password))
        list_player2 = response.json()
        count_player = len(list_player1) if len(list_player2) > len(list_player1) else len(list_player2)
        for i in range(count_player):
            assert list_player1[i] == list_player2[i], \
                print(f"The data from the server is changed for each get first time: "
                      f"{list_player1[i]} second time: {list_player2[i]}")

    def test_id_of_player(self,start_server):
        player_list_3_page = []
        for i in range(3):
            response = requests.get(url_server+str(i+1), auth=HTTPBasicAuth(username, password))
            player_list_3_page.append(response.json())
        for i in range(2):
            assert player_list_3_page[i][-1]["ID"] == player_list_3_page[i+1][0]["ID"]-1, \
                print("Each page is missing the last player")

    def test_page_17_null(self, start_server):
        response = requests.get(url_server + str(17), auth=HTTPBasicAuth(username, password))
        list_player = response.json()
        for dict_plyer in list_player:
            for k, v in dict_plyer.items():
                assert v != "null", print(f"no value in {dict_plyer}")
