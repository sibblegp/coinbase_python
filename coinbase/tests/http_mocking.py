import httpretty
import json
import unittest


def setUp_method_with_http_mocking(test_class):

    original_setUp = test_class.setUp if hasattr(test_class, 'setUp') else None

    def new_setUp(self):
        httpretty.enable()
        self.addCleanup(httpretty.disable)
        if original_setUp:
            original_setUp(self)

    test_class.setUp = new_setUp

    return test_class


def is_TstCase(x):
    try:
        return issubclass(x, unittest.TestCase)
    except TypeError:
        return False


def with_http_mocking(x):

    if is_TstCase(x):
        return setUp_method_with_http_mocking(x)

    return httpretty.httprettified(x)


def last_request_body():
    return httpretty.last_request().body


def last_request_json():
    return json.loads(last_request_body().decode('UTF-8'))


def last_request_params():
    return httpretty.last_request().querystring


def mock_http(header, response_body, content_type='text/json'):

    method, uri = header.split(' ', 1)
    httpretty.register_uri(
        method=method,
        uri=uri,
        body=response_body,
        content_type=content_type,
    )
