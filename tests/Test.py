# content of test_sample.py

from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}




# class TestClassDemoInstance:
#     value = 0

#     def test_one(self):
#         self.value = 1
#         assert self.value == 1

#     def test_two(self):
#         assert self.value == 1


# class TestClass:
#     def test_one(self):
#         x = "this"
#         assert "h" in x

#     def test_two(self):
#         x = "hello"
#         assert hasattr(x, "check")

        


# import pytest

# def f():
#     raise SystemExit(1)

# def test_mytest():
#     with pytest.raises(SystemExit):
#         f()


# def func(x):
#     return x+1

# def test_answer():
#     assert func(3) == 5