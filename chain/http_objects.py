try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

try:
    import httplib
except ImportError:
    import http.client as httplib


class Request(object):
    def __init__(self, host=None, method=None, url=None, headers=None,
                 cookies=None, body=None, query=None, **kwargs):

        headers = {} if headers is None else headers
        cookies = {} if cookies is None else cookies
        body = '' if body is None else body
        query = {} if query is None else query
        host = '' if host is None else host

        self.host = host
        self.method = method
        self.url = url
        self.headers = headers
        self.cookies = cookies
        self.body = body
        self.query = query

    def send(self, url, query=None, body=None, **kwargs):
        if url:
            self.url = url
        return self._send(query, body)

    def _send(self, query=None, body=None):
        if query is None:
            query = self.query

        if body is None:
            body = self.body

        self.build_url(query)

        connection = httplib.HTTPConnection(self.host)
        connection.request(
            self.method, self.url, body, self.headers
        )

        return self.build_response(connection.getresponse())

    def build_url(self, query):
        if query:
            self.url = '{}?{}'.format(
                self.url, self.build_query_string(query))

    @staticmethod
    def build_query_string(query):
        return urlencode(query)

    def build_response(self, response):
        return Response(response, self)


class Response(object):
    """
    Provides an high level reference to the response object, including
     things like getting the headers, response status, body in json,
     raw body and the raw httplib response object
    """
    def __init__(self, raw_response, request=None):
        self.raw_response = raw_response
        self.request_sent = request
