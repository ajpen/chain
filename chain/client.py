from .http_objects import Request


class RequestBuilder(object):

    def __init__(self, url, request_obj):
        self.___url___ = url
        self.___rqo___ = request_obj

    def __getattr__(self, name):
        url = '{}/{}'.format(self.___url___, name)
        return RequestBuilder(url, self.___rqo___)

    def __call__(self, *args, **kwargs):
        return self.___rqo___.send_to_url(
            self.___url___, *args, **kwargs)


# TODO: May need to move pre_request_callback up to the Request class,
# so that it is called just before the request is sent
class Client(object):

    methods = ('GET', 'POST', 'PUT', 'DELETE')

    _default_headers = {'content-type': 'application/json'}

    def __init__(self, host, headers=None, cookies=None,
                 pre_request_callback=lambda: True,
                 use_default_headers=True, default_method='GET'):
        """
        Client that provides an intuitive interface to building andconfiguring
        requests. 
        :param host: the address (port included) of the API/resource. 
               e.g. 'someservice.com' or 'localhost:80'
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
        self.host = host
        if cookies is None:
            cookies = {}
        self.cookies = cookies
        if use_default_headers or headers is None:
            headers = self._default_headers
        self.headers = headers
        self.pre_request_callback = pre_request_callback
        self.default_method = default_method

    def __getattr__(self, name):
        """
        Where the magic happens! If the attribute requested is a method name
        (get, post, etc), start the build with that particular method, else
        do what you always do.
        :param name:
        :return: RequestBuilder or raises an AttributeError
        """
        method = name.upper()
        if method in Client.methods:
            return self._start_build(method)
        raise AttributeError('type {} has no attribute {}'.format(type(self), name))

    def set_pre_request_callback(self, callback):
        """
        Set callback that is called before evey request.
        :param callback: called before each request. 
                         Receives an instance of Client as the first parameter
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
        self.host = url

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
        if not endpoint:
            endpoint = ''

        if not query:
            query = {}

        if not body:
            body = {}

        request = self.prepare_request(
            endpoint,
            method=self.default_method
        )
        return request.send(query, body)

    def prepare_request(self, url, headers=None,
                        method=None):
        """

        :return: request object 
        """
        self.run_pre_request()

        if not method:
            method = self.default_method
        if not headers:
            headers = self.prepare_request_headers()

        return Request(self.host, url, method=method,
                       headers=headers)

    def run_pre_request(self):
        if self.pre_request_callback:
            self.pre_request_callback()

    def prepare_request_headers(self):
        headers = dict(self.headers)
        headers['Cookie'] = self.prepare_request_cookie()
        return headers

    def prepare_request_cookie(self):
        cookie_list = ['{}={};'.format(k, v) for k, v in self.cookies.items()]
        return ' '.join(cookie_list)

    def _start_build(self, method='GET'):
        self.run_pre_request()
        request_obj = self.prepare_request('', method=method)
        return RequestBuilder('', request_obj)
