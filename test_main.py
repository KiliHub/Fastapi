from fastapi.testclient import TestClient
from .main import app
import unittest

client = TestClient(app)

assertions = ['id', 'first_name', 'last_name', 'middle_name', 'gender', 'roles']
runs = [{"id":"6179079b-fc4a-465c-9e08-19690a749a95","first_name":"Jamila","last_name":"Ahmed","middle_name":"None","gender":"female","roles":["student"]},{"id":"ad252d19-42ea-482f-a103-2d5fcbf57e70","first_name":"Alex","last_name":"Jones","middle_name":"None","gender":"male","roles":["admin","user"]}]

class testcases(unittest.TestCase):

    def test_read_main(self):
        self.response = client.get("/api/v1/users")
        assert self.response.status_code == 200
       
        for run in runs:
            for assertion in assertions:
                if isinstance(run.get(assertion), type(list)):
                    liste = run.get(assertion)
                    for i in liste:
                        assert str(i) in str(self.response.json())
                else:
                    t = run.get(assertion)
                    assert str(t) in str(self.response.json())

    def test(self):
        self.response = client.get("/")
        assert self.response.status_code == 200
        assert self.response.json() == {"Hello":"Kili"}
        