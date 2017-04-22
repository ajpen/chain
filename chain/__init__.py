"""chain - An expressive clean way to interact with RESTful APIs."""

__version__ = '0.1.0'
__author__ = 'Anfernee Jervis <anferneejervis@gmail.com>'
__all__ = []


try:
    import httplib
except ImportError:
    import http.client as httplib


class Client(object):

    def __init__(self, url):
        self.url = url

    def __getattr__(self, name):
        url = '{}/{}'.format(self.url, name)
        return Client(url)


class Request(object):
    def __init__(self, url, headers=None, query=None, body=None):
        self.url = url
        self.headers = headers
        self.query = query
        self.body = body
        self.method = None
        self.authentication_headers = {}
        self.authentication_callback = self.default_authentication_callback
        self.response = None

    @staticmethod
    def default_authentication_callback(*args, **kwargs):
        return {}

    @staticmethod
    def default_headers():
        return {'content-type': 'application/json'}

    def set_authentication_callback(self, callback):
        self.authentication_callback = callback

    def prepare_authentication_headers(self):
        if self.authentication_headers:
            self.headers.update(self.authentication_headers)
        else:
            self.headers.update(self.authentication_callback(self))

    def send(self):
        pass


class Response(object):
    """
    Provides an high level reference to the response object, including
     things like getting the headers, response status, body in json,
     raw body and the raw httplib response object
    """
    pass


class Get(Request):

    def send(self):
        self.method = 'GET'
        super(Get, self).send()


class Post(Request):

    def send(self):
        self.method = 'POST'
        super(Post, self).send()


class Put(Request):

    def send(self):
        self.method = 'PUT'
        super(Put, self).send()


class Delete(Request):

    def send(self):
        self.method = 'GET'
        super(Delete, self).send()