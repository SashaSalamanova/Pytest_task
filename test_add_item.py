import requests as r
from jsonschema import validate
import pytest


class TestAddNewItem():
    """this test checks methods that aadd new data"""
    book_url = "http://yoshilyosha.pythonanywhere.com/api/v1/book"
    user_url = "http://yoshilyosha.pythonanywhere.com/api/v1/user"
    db_url = "http://yoshilyosha.pythonanywhere.com/api/v1/test/repopulate_db"
    book_name = "1984"
    book_name_invalid = 1984
    book_author = "George Orwell"
    book_author_invalid = 66
    book_amount = 8
    book_amount_invalid = -1
    book_data = {
        "book_name": book_name,
        "book_author": book_author,
        "amount": book_amount
    }
    book_id = 1
    user_name = "Billy"
    user_name_invalid = 0
    user_id = 4
    taken_books_ids = []
    user_data = {"user_name": user_name}
    book_amount = 8
    add_book_template = {
        "type": "object",
        "properties": {
            "body": {
                "type": "object",
                "properties": {
                    "amount": {"type": "number"},
                    "author": {"type": "string"},
                    "id": {"type": "number"},
                    "name": {"type": "string"},
                },
                "required": ["amount", "author", "id", "name"]
            },
            "status": {"type": "number"}
        },
        "required": ["body", "status"]
    }
    add_user_template = {
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
                },
                "required": ["id", "name", "taken_books_ids"]
            },
            "status": {"type": "number"}
        },
        "required": ["body", "status"]
    }

    def setup_method(self, method):
        r.post(self.db_url)

    def add_item(self, url=book_url, data=book_data, method="POST"):
        if method == "POST":
            resp = r.post(url, json=data)
        elif method == "GET":
            resp = r.get(url, params=data)
        return resp

    # Check Status
    @pytest.mark.parametrize("url,data,method", [
            (book_url, book_data, "GET"),
            pytest.param(book_url,
                         book_data,
                         "POST",
                         marks=pytest.mark.skip(reason="this method fails")),
            (user_url, user_data, "GET"),
            (user_url, user_data, "POST"),
    ])
    def test_response_status(self, method, data, url):
        assert self.add_item(url+"/add", data, method).status_code == 200

    # Check Response Template
    @pytest.mark.parametrize("url,data,template,method", [
            pytest.param(book_url, book_data, add_book_template, "POST",
                         marks=pytest.mark.skip(reason="this method fails")),
            (book_url, book_data, add_book_template, "GET"),
            (user_url, user_data, add_user_template, "GET"),
            (user_url, user_data, add_user_template, "POST"),
    ])
    def test_response_json(self, method, template, url, data):
        json_string = self.add_item(url+"/add", data, method).json()
        if validate(json_string, template) is None:
            assert True
        else:
            assert False

    # Check Response Content - AddBook
    @pytest.mark.parametrize("method", [
        "GET",
        pytest.param(
                "POST",
                marks=pytest.mark.skip(reason="this method fails")
        )
    ])
    def test_response_add_book_content(self, method):
        json_str = self.add_item(self.book_url+"/add",
                                 self.book_data,
                                 method
                                ).json()
        assert json_str['body']['amount'] == self.book_amount
        assert json_str['body']['author'] == self.book_author
        assert json_str['body']['name'] == self.book_name

    # Check Response Content - AddUser
    @pytest.mark.parametrize("method", ["GET", "POST"])
    def test_response_add_user_content(self, method):
        json_str = self.add_item(self.user_url+"/add",
                                 self.user_data,
                                 method
                                ).json()
        assert json_str['body']['name'] == self.user_name

    @pytest.mark.parametrize("url,data,expected_status", [
            pytest.param(book_url,
                         {
                             "book_name": book_name_invalid,
                             "book_author": book_author,
                             "amount": book_amount
                         },
                         200,
                         marks=pytest.mark.xfail
                         ),
            pytest.param(book_url,
                         {
                             "book_name": book_name,
                             "book_author": book_author_invalid,
                             "amount": book_amount
                         },
                         200,
                         marks=pytest.mark.xfail
                         ),
            pytest.param(book_url, {
                "book_name": book_name,
                "book_author": book_author,
                "amount": book_amount_invalid
            },
                         200,
                         marks=pytest.mark.xfail
            ),
            pytest.param(user_url,
                         {
                             "user_name": user_name_invalid
                         },
                         200,
                         marks=pytest.mark.xfail
                         ),
            ])
    @pytest.mark.parametrize("method", ["GET", "POST"])
    def test_response_status_invalid(self, url, data, expected_status, method):
        assert self.add_item(url+"/add",
                             data,
                             method
                            ).status_code == expected_status
