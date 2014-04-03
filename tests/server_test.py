__author__ = 'wre9fz'
import requests
import json
from random import randint
from unittest import TestCase

HOST = 'http://127.0.0.1:5000/'
USERNAME = "OneDir"
PASSWORD = "test"

class TestServer(TestCase):

    def setUp(self):
        url = HOST + "session"
        data = {'username': USERNAME, 'password': PASSWORD}
        headers = {'Content-Type': 'application/json'}
        r = requests.post(url, data=json.dumps(data), headers=headers)
        self.cookies = r.cookies

    def test_post_file(self):
        url = HOST + "file/test"
        headers = {'Content-Type': 'application/json'}
        r = requests.post(url, files={'file': open('test_upload.txt', 'rb')}, cookies=self.cookies)
        self.assertEqual(r.json()['result'], 1)

        url = HOST + "file"
        headers = {'Content-Type': 'application/json'}
        r = requests.post(url, files={'file': open('test_upload.txt', 'rb')}, cookies=self.cookies)
        self.assertEqual(r.json()['result'], 1)

    def test_get_file(self):
        url = HOST + "file/test/test_upload.txt"
        r = requests.get(url, cookies=self.cookies)
        self.assertEqual(r.text, "UploadTest")
        url = HOST + "file/fake_file.txt"
        r = requests.get(url, cookies=self.cookies)
        self.assertEqual(r.json()['result'], -1)

    def test_registration(self):
        url = HOST + "register"
        random_int = randint(0,10000)
        data = {'username': random_int, 'password': 'password', 'email': random_int}
        headers = {'Content-Type': 'application/json'}
        r = requests.post(url, data=json.dumps(data), headers=headers)
        self.assertEqual(r.json()['result'], str(random_int))

    def test_login(self):
        url = HOST + "session"
        data = {'username': USERNAME, 'password': PASSWORD}
        headers = {'Content-Type': 'application/json'}
        r = requests.post(url, data=json.dumps(data), headers=headers)
        self.assertEquals(len(r.cookies), 1)
        data = {'username': "Fake User", 'password': "Fake Password"}
        r = requests.post(url, data=json.dumps(data), headers=headers)
        self.assertEquals(r.json()['result'], -1)

    def test_logout_and_auth(self):
        self.reset_session()
        url = HOST + "session"
        headers = {'Content-Type': 'application/json'}
        r = requests.delete(url, cookies=self.cookies, headers=headers)
        self.assertEqual(r.json()['result'], USERNAME)
        url = HOST + "file/test_upload.txt"
        r = requests.get(url)
        self.assertEqual(r.json()['result'], -2)
        self.reset_session()

    def reset_session(self):
        url = HOST + "session"
        data = {'username': USERNAME, 'password': PASSWORD}
        headers = {'Content-Type': 'application/json'}
        r = requests.post(url, data=json.dumps(data), headers=headers)
        self.cookies = r.cookies

    def test_list(self):
        url = HOST + "list"
        headers = {'Content-Type': 'application/json'}
        r = requests.get(url, headers=headers, cookies=self.cookies)
        files = json.loads(r.text)
        self.assertEqual(files['files'][0]['name'], 'test_upload.txt')
