import unittest
import requests

post_url = "https://reqres.in/api/users"
get_url_single_user = "https://reqres.in/api/users/2"
get_url_user_not_found = "https://reqres.in/api/users/23"
post_register_url = "https://reqres.in/api/register"
delay_url = "https://reqres.in/api/users?delay=3"

class TestAPI(unittest.TestCase):

    def test_get_list_users(self):
        response = requests.get(url=post_url)
        assert response.status_code == 200
        assert response.json()["page"] == 1
        assert response.json()["per_page"] == 6
        assert response.json()["total"] == 12
        assert response.json()["total_pages"] == 2

    def test_get_single_user(self):
        response = requests.get(url=get_url_single_user)
        assert response.status_code == 200
        assert response.json()["data"]["id"] == 2
        assert response.json()["data"]["email"] == "janet.weaver@reqres.in"
        assert response.json()["data"]["first_name"] == "Janet"
        assert response.json()["data"]["last_name"] == "Weaver"

    def test_get_single_user_not_found(self):
        response = requests.get(url=get_url_user_not_found)
        assert response.status_code == 404
        assert response.json() == {}

    def test_create_user(self):
        post_body = {
            "name" : "Agnieszka",
            "job" : "QA"
        }
        response = requests.post(url=post_url, json=post_body)
        assert response.status_code == 201
        assert response.json()["name"] == "Agnieszka"
        assert response.json()["job"] == "QA"
        assert int(response.json()["id"]) > 0
        assert response.json()["createdAt"] is not None

    def test_update_user(self):
        put_body = {
            "name" : "Agnieszka",
            "job" : "QA engineer"
            }
        response = requests.put(url=get_url_single_user, json=put_body)
        assert response.status_code == 200
        assert response.json()["updatedAt"] is not None

    def test_delete_user(self):
        response = requests.delete(url=get_url_single_user)
        assert response.status_code == 204

    def test_register_successful(self):
        post_register_body = {
            "email": "janet.weaver@reqres.in",
            "password": "password"
            }
        response = requests.post(url=post_register_url, json=post_register_body)
        assert response.status_code == 200
        assert response.json()["id"] > 0
        assert response.json()["token"] is not None

    def test_register_unsuccessful(self):
        post_register_body = {
            "email": "janet.weaver@reqres.in"
            }
        response = requests.post(url=post_register_url, json=post_register_body)
        assert response.status_code == 400
        assert response.json() == {
            "error": "Missing password"
            }

    def test_delay_response(self):
        response = requests.get(url=delay_url)
        assert response.status_code == 200
        assert (response.elapsed.total_seconds()) > 3

if __name__ == '__main__':
    unittest.main()

