import requests as r
from jsonschema import validate
import pytest


class TestGetListOfItems():
    """This test checks methods for list of items"""
    books_url = "http://yoshilyosha.pythonanywhere.com/api/v1/books"
    users_url = "http://yoshilyosha.pythonanywhere.com/api/v1/users"
    books_temp_dict = {
        "type": "object",
        "properties": {
            "body": {
                "type": "object",
                "properties": {
                    "books": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "amount": {"type": "number"},
                                "author": {"type": "string"},
                                "id": {"type": "number"},
                                "name": {"type": "string"}
                            }
                        }
                    }
                },
                "required": ["books"]
            },
            "status": {"type": "number"}
        },
        "required": ["body", "status"]
    }
    users_temp_dict = {
        "type": "object",
        "properties": {
            "body": {
                "type": "object",
                "properties": {
                    "users": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "number"},
                                "name": {"type": "string"},
                                "taken_books_ids": {
                                "type": "array",
                                "items": {"type": "number"}
                                }
                            }
                        }
                    }
                },
                "required": ["users"]
            },
            "status": {"type": "number"}
        },
        "required": ["body", "status"]
    }

    def setup_class(cls):
        r.post("http://yoshilyosha.pythonanywhere.com/api/v1/test/repopulate_db")

    def get_response(self, url=books_url, method="GET"):
        if method == "GET":
            response = r.get(url)
        elif method == "POST":
            response = r.post(url)
        return response

    # Test response status
    @pytest.mark.parametrize("method", ["GET", "POST"])
    @pytest.mark.parametrize("url", [books_url, users_url])
    def test_response_status(self, method, url):
        assert self.get_response(url, method).status_code == 200

    # Test response json format
    @pytest.mark.parametrize("url,template", [
    (books_url, books_temp_dict),
    (users_url, users_temp_dict),
    ])
    @pytest.mark.parametrize("method", ["GET", "POST"])
    def test_response_json_teplate(self, url, template, method):
        json_string = self.get_response(url, method).json()
        if validate(json_string, template) is None:
            assert True
        else:
            assert False
