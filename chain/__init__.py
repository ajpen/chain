"""chain - An expressive clean way to interact with RESTful APIs."""

__version__ = '0.1.0'
__author__ = 'Anfernee Jervis <anferneejervis@gmail.com>'
__all__ = []

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

try:
    import httplib
except ImportError:
    import http.client as httplib


class RequestBuilder(object):

    def __init__(self, url, request_obj):
        self.___url___ = url
        self.___rqo___ = request_obj

    def __getattr__(self, name):
        url = '{}/{}'.format(self.___url___, name)
        return RequestBuilder(url, self.___rqo___)

    def __call__(self, *args, **kwargs):
        return self.___rqo___.send(self.___url___, *args, **kwargs)


class Request(object):
    def __init__(self, url, method='GET', headers=None, query=None, body=None):
        self.url = url
        self.headers = headers
        self.query = query
        self.body = body
        self.method = method
        self.response = None

    def send(self):
        pass


class Response(object):
    """
    Provides an high level reference to the response object, including
     things like getting the headers, response status, body in json,
     raw body and the raw httplib response object
    """
    def __init__(self, raw_response, request=None):
        self.raw_response = raw_response
        self.request_sent = request


class Client(object):

    _default_headers = {'content-type': 'application/json'}

    def __init__(self, base_url, headers=None, cookies=None,
                 pre_request_callback=None, use_default_headers=False, default_method='GET'):
        """
        Client that provides an intuitive interface to building andconfiguring
        requests. 
        :param base_url: url that resources belong to. 
               e.g. 'http://someservice.com' 
        :param headers: Any headers that will be passed to all requests unless
               explicitly changed with the 'set_headers' method
        :param cookies: Any cookies that will be passed to all requests unless
               explicitly changed with the 'set_cookies' method. Cookies are
               automatically merged into headers before each request. Must be
               dict with key value pairs.
        :param pre_request_callback: executed before each request. Can be used
               for changing headers, authentication, etc
        :param use_default_headers: If True, each request will use the default
                                    header 'content-type': 'application/json'
                                    if headers is not specified.
        :param default_method: sets the default method to use when the 
                               send_request method is executed. Defaults to
                               'GET'
        """
        self.url = base_url
        self.cookies = cookies
        if use_default_headers:
            headers = self._default_headers
        self.headers = headers
        self.pre_request_callback = pre_request_callback
        self.default_method = default_method

    def set_pre_request_callback(self, callback):
        """
        Set callback that is called before evey request.
        :param callback: called before each request. 
                         Receives an instance of Client as the first parameter.
                         to allow modification of headers, cookies, etc
        :return: None 
        """
        self.pre_request_callback = callback

    def set_headers(self, headers):
        self.headers = headers

    def set_cookies(self, cookies):
        self.cookies = cookies

    def set_default_method(self, method):
        self.default_method = method

    def change_base_url(self, url):
        self.url = url

    def copy_headers(self):
        """
        returns a copy of the default headers
        :return: default headers (dict)
        """
        return dict(self.headers)

    def copy_cookies(self):
        """
        returns a copy of the default cookies
        :return: default cookies (dict)
        """
        return dict(self.cookies)

    def send_request(self, endpoint=None, query=None, body=None):
        """
        Sends a request to the endpoint using the default method
        :param endpoint: target endpoint e.g. '/toast'
        :param query: arguments for the query string
        :param body: the request body
        :return: Response object
        """
        target_url = '{}{}'.format(self.url, endpoint)

        request = self.prepare_request(
            target_url,
            method=self.default_method,
            query=query,
            body=body
        )
        return request.send()

    def prepare_request(self, url, headers=None,
                        method=None, query=None,body=None):
        """

        :return: request object 
        """
        self.run_pre_request()

        if not method:
            method = self.default_method
        if not headers:
            headers = self.prepare_request_headers()

        return Request(url, method=method,
                       headers=headers, query=query, body=body)

    def run_pre_request(self):
        if self.pre_request_callback:
            self.pre_request_callback()

    def prepare_request_headers(self):
        headers = dict(self.headers).copy()
        headers['Cookie'] = self.prepare_request_cookie()
        return headers

    def prepare_request_cookie(self):
        cookie_list = ['{}={};'.format(k, v) for k, v in self.cookies.items()]
        return ' '.join(cookie_list)