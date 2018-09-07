import requests as r
from jsonschema import validate
import pytest


class TestGetItemById():
    """this test checks methods that access data"""
    book_url = "http://yoshilyosha.pythonanywhere.com/api/v1/book"
    user_url = "http://yoshilyosha.pythonanywhere.com/api/v1/user"
    book_id = 1
    book_invalid_id = 9999
    book_payload = {"book_id": book_id}
    book_invalid_payload = {"book_id": "kgjbng"}
    book_not_existing_id_payload = {"book_id": book_invalid_id}
    user_id = 1
    user_invalid_id = 77777
    user_payload = {"user_id": user_id}
    user_invalid_payload = {"user_id": "aepdkc"}
    user_not_existing_id_payload = {"user_id": user_invalid_id}
    user_tamplate_dict = {
        "type": "object",
        "properties": {
            "body": {
                "type": "object",
                "properties": {
                    "id": {"type": "number"},
                    "name": {"type": "string"},
                    "taken_books_ids": {
                            "type": "array",
                            "items": {"type": "number"}
                    }
                }
            },
            "status": {"type": "number"}
        },
        "required": ["body", "status"]
    }
    book_tamplate_dict = {
        "type": "object",
        "properties": {
            "body": {
                "type": "object",
                "properties": {
                    "amount": {"type": "number"},
                    "author": {"type": "string"},
                    "id": {"type": "number"},
                    "name": {"type": "string"}
                },
                "required": ["amount", "author", "id", "name"]
            },
            "status": {"type": "number"}
        },
        "required": ["body", "status"]
    }

    def setup_class(cls):
        r.post("http://yoshilyosha.pythonanywhere.com/api/v1/test/repopulate_db")

    def get_response(self, url=book_url, payload=book_payload, method="GET"):
        if method == "GET":
            response = r.get(url, params=payload)
        elif method == "POST":
            response = r.post(url, json=payload)
        return response

    @pytest.mark.parametrize("url,payload,status_expexted", [
                            (book_url, book_payload, 200),
                            (user_url, user_payload, 200),
                            pytest.param(book_url,
                                         book_invalid_payload,
                                         400,
                                         marks=pytest.mark.skip(reason="fail")
                                         ),
                            (user_url, user_invalid_payload, 400),
                            (book_url, book_not_existing_id_payload, 500),
                            (user_url, user_not_existing_id_payload, 500),
    ])
    @pytest.mark.parametrize("method", ["GET", "POST"])
    def test_response_status(self, url, method, payload, status_expexted):
        assert self.get_response(url,
                                 payload,
                                 method).status_code == status_expexted

    @pytest.mark.parametrize("url,template,payload,item_id", [
            (book_url, book_tamplate_dict, book_payload, book_id),
            (user_url, user_tamplate_dict, user_payload, user_id),
    ])
    @pytest.mark.parametrize("method", ["GET", "POST"])
    def test_response_json_teplate(self, url, template, method,
                                   payload, item_id):
        json_string = self.get_response(url, payload, method).json()
        if validate(json_string, template) is None:
            assert True
        else:
            assert False
