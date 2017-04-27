try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

try:
    import httplib
except ImportError:
    import http.client as httplib


class Request(object):
    def __init__(self, host, url, method='GET', headers=None, timeout=None):
        self.host = host
        self.url = url
        self.headers = headers
        self.method = method
        self.response = None
        if timeout:
            self.timeout = timeout

    def send_to_url(self, url, query=None, body=None):
        if url is None:
            url=''

        self.url = url
        return self.send(query, body)

    def send(self, query=None, body=None):
        if query is None:
            query = dict()

        if body is None:
            body = ''

        self.build_url(query)
        connection = httplib.HTTPConnection(self.host)
        connection.request(
            self.method, self.url, body, self.headers
        )
        response = connection.getresponse()

        return self.build_response(response)

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
