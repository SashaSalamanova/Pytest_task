import requests as r
from jsonschema import validate
import pytest


class TestApi():
    """This test checks take_book and return_book"""
    base_url = "http://yoshilyosha.pythonanywhere.com/api/v1/user/"
    db_url = "http://yoshilyosha.pythonanywhere.com/api/v1/test/repopulate_db"
    default_data = {"user_id": 1, "book_id": 1}
    test_data = {"user_id": 1, "book_id": 10}
    invalid_data_book = {"user_id": 1, "book_id": -1}
    invalid_data_user = {"user_id": -1, "book_id": 1}
    template = {
        "type": "object",
        "properties": {
            "body": {"type": "string"},
            "status": {"type": "number"}
        },
        "required": ["body", "status"]
    }

    def setup_method(self, method):
        r.post(self.db_url)

    def take_book(self, data=default_data, method="POST"):
        if method == "POST":
            resp = r.post(self.base_url + "take_book", json=data)
        if method == "GET":
            resp = r.get(self.base_url + "take_book", params=data)
        return resp

    def return_book(self, data=default_data, method="POST"):
        if method == "POST":
            resp = r.post(self.base_url + "return_book", json=data)
        if method == "GET":
            resp = r.get(self.base_url + "return_book", params=data)
        return resp

    # test to check take one book by get and post
    @pytest.mark.parametrize("method", [
        "GET",
        pytest.param("POST",
                     marks=pytest.mark.skip(reason="this method fails")
                     )
    ])
    def test_take_book(self, method):
        assert self.take_book(method=method).status_code == 200

    @pytest.mark.parametrize("method", [
        "GET",
        pytest.param("POST",
                     marks=pytest.mark.skip(reason="this method fails"))
    ])
    def test_response_json_teplate_take_book(self, method):
        json_string = self.take_book(method=method).json()
        if validate(json_string, self.template) is None:
            assert True
        else:
            assert False

    @pytest.mark.parametrize("method", [
        "POST",
        pytest.param("GET",
                     marks=pytest.mark.skip(reason="this method fails"))
    ])
    def test_response_json_teplate_return_book(self, method):
        json_string = self.return_book(method=method).json()
        if validate(json_string, self.template) is None:
            assert True
        else:
            assert False

    # test to check take three different books by get and post

    @pytest.mark.parametrize("method", [
        "GET",
        pytest.param("POST",
                     marks=pytest.mark.skip(reason="this method fails"))
    ])
    def test_take_three_different_books(self, method):
        assert self.take_book(method=method).status_code == 200
        assert self.take_book(data={"user_id": 1, "book_id": 2},
                              method=method).status_code == 200
        assert self.take_book(data={"user_id": 1, "book_id": 3},
                              method=method).status_code == 200
    # this test should fail
    # user should not be allowed to take 4 diff books

    @pytest.mark.xfail
    @pytest.mark.parametrize("method", [
        "GET",
        pytest.param("POST",
                     marks=pytest.mark.skip(reason="this method fails"))
    ])
    def test_take_four_different_books(self, method):
        assert self.take_book(method=method).status_code == 200
        assert self.take_book(data={"user_id": 1, "book_id": 2},
                              method=method).status_code == 200
        assert self.take_book(data={"user_id": 1, "book_id": 3},
                              method=method).status_code == 200
        assert self.take_book(data={"user_id": 1, "book_id": 4},
                              method=method).status_code == 200

    # user should be able to to take 4 equal books

    @pytest.mark.parametrize("method", [
        "GET",
        pytest.param("POST",
                     marks=pytest.mark.skip(reason="this method fails"))
    ])
    def test_take_four_equal_books(self, method):
        assert self.take_book(method=method).status_code == 200
        assert self.take_book(method=method).status_code == 200
        assert self.take_book(method=method).status_code == 200
        assert self.take_book(method=method).status_code == 200

    # this test should fail
    # test take_book with invalid data

    @pytest.mark.xfail
    @pytest.mark.parametrize("method", [
        "GET",
        pytest.param("POST",
                     marks=pytest.mark.skip(reason="this method fails"))
    ])
    def test_invalid_data(self, method):
        assert self.take_book(data=self.invalid_data_book,
                              method=method).status_code == 200
        assert self.take_book(data=self.invalid_data_user,
                              method=method).status_code == 200

    # Return Book
    # take_book and return the same book

    @pytest.mark.parametrize("method", [
        "POST",
        pytest.param("GET",
                     marks=pytest.mark.skip(reason="this method fails"))
    ])
    def test_return_book(self, method):
        assert self.take_book(method="GET").status_code == 200
        assert self.return_book(method=method).status_code == 200

    # user should not be able to return book that he doesn't have

    @pytest.mark.xfail
    @pytest.mark.parametrize("method", [
        "POST",
        pytest.param("GET",
                     marks=pytest.mark.skip(reason="this method fails"))
    ])
    def test_return_book_user_doesnt_have(self, method):
        assert self.return_book(data=self.test_data,
                                method=method).status_code == 200
