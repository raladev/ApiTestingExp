import re
import requests
from tests.conftest import base_url


class client(object):

    @staticmethod
    def request(method, address, session=None,
                params=None, headers=None, cookies=None, data=None, json=None, allow_redirects=True, timeout=30):

        if headers is None:
            headers = {}
        if "User-Agent" not in headers:
            headers["User-Agent"] = "Ultra-User-Agent"
        if session is None:
            session = requests.Session()

        request = requests.Request(method, address,
                                   params=params, headers=headers, cookies=cookies, json=json, data=data)

        try:
            response = session.send(request=request.prepare(), allow_redirects=allow_redirects, timeout=timeout)
        except requests.exceptions.Timeout:
            raise TimeoutError("Connection to %s timed out" % address)
        except requests.exceptions.ConnectionError:
            raise ConnectionError("Connection to %s failed" % address)
        except BaseException:
            raise

        return HTTPResponse(response)

    @staticmethod
    def get(path='', address=base_url, **kwargs):
        return client.request("GET", address + path, **kwargs)

    @staticmethod
    def post(path='', address=base_url, **kwargs):
        return client.request("POST", address + path, **kwargs)

    @staticmethod
    def put(path='', address=base_url, **kwargs):
        return client.request("PUT", address + path, **kwargs)

    @staticmethod
    def delete(path='', address=base_url, **kwargs):
        return client.request("DELETE", address + path, **kwargs)


class HTTPResponse(object):
    def __init__(self, py_response):

        self.url = py_response.url
        self.method = py_response.request.method
        self.status_code = int(py_response.status_code)
        self.reason = py_response.reason

        self.headers = dict(py_response.headers)
        self.cookies = dict(py_response.cookies)

        self.text = py_response.text
        self.content = py_response.content

        self.elapsed = py_response.elapsed

        self._response = py_response
        self._request = py_response.request

    def json(self):
        return self._response.json()

    def __eq__(self, other):
        return isinstance(other, self.__class__) \
               and self.status_code == other.status_code \
               and self.method == other.method \
               and self.url == other.url \
               and self.reason == other.reason \
               and self.headers == other.headers \
               and self.cookies == other.cookies \
               and self.text == other.text \
               and self.content == other.content

    def __repr__(self):
        params = (self.method, self.url, self.status_code, self.reason)
        return "%s %s => %s %s" % params

    def assert_ok(self, msg=None):
        if self.status_code >= 400:
            msg = msg or "Request to %s didn't succeed (%s)" % (self.url, self.status_code)
            raise AssertionError(msg)
        return self

    def assert_failed(self, msg=None):
        if self.status_code < 400:
            msg = msg or "Request to %s didn't fail (%s)" % (self.url, self.status_code)
            raise AssertionError(msg)
        return self

    def assert_2xx(self, msg=None):
        if not 200 <= self.status_code < 300:
            msg = msg or "Response code isn't 2xx, it's %s" % self.status_code
            raise AssertionError(msg)
        return self

    def assert_3xx(self, msg=None):
        if not 300 <= self.status_code < 400:
            msg = msg or "Response code isn't 3xx, it's %s" % self.status_code
            raise AssertionError(msg)
        return self

    def assert_4xx(self, msg=None):
        if not 400 <= self.status_code < 500:
            msg = msg or "Response code isn't 4xx, it's %s" % self.status_code
            raise AssertionError(msg)
        return self

    def assert_5xx(self, msg=None):
        if not 500 <= self.status_code < 600:
            msg = msg or "Response code isn't 5xx, it's %s" % self.status_code
            raise AssertionError(msg)
        return self

    def assert_status_code(self, code, msg=None):
        actual = str(self.status_code)
        expected = str(code)
        if actual != expected:
            msg = msg or "Actual status code (%s) didn't match expected (%s)" % (actual, expected)
            raise AssertionError(msg)
        return self

    def assert_not_status_code(self, code, msg=None):
        actual = str(self.status_code)
        expected = str(code)
        if actual == expected:
            msg = msg or "Actual status code (%s) unexpectedly matched" % actual
            raise AssertionError(msg)
        return self

    def assert_in_body(self, member, msg=None):
        if member not in self.text:
            msg = msg or "%r wasn't found in response body" % member
            raise AssertionError(msg)
        return self

    def assert_not_in_body(self, member, msg=None):
        if member in self.text:
            msg = msg or "%r was found in response body" % member
            raise AssertionError(msg)
        return self

    def assert_has_header(self, header, msg=None):
        if header not in self.headers:
            msg = msg or "Header %s wasn't found in response headers: %r" % (header, self.headers)
            raise AssertionError(msg)
        return self

    def assert_header_value(self, header, value, msg=None):
        self.assert_has_header(header)
        actual = self.headers[header]
        if actual != value:
            msg = msg or "Actual header value (%r) isn't equal to expected (%r)" % (actual, value)
            raise AssertionError(msg)
        return self

    def extract_regex(self, regex, default=None):
        extracted_value = default
        for item in re.finditer(regex, self.text):
            extracted_value = item
            break
        return extracted_value
