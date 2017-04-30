try:
    from plugins import RequestsRequest as Request
except:
    raise ImportError("requests package not found")


class RequestBuilder(object):

    def __init__(self, url, request_obj):
        self.___url___ = url
        self.___rqo___ = request_obj

    def __getattr__(self, name):
        url = '{}/{}'.format(self.___url___, name)
        return RequestBuilder(url, self.___rqo___)

    def __call__(self, *args, **kwargs):
        return self.___rqo___.send(
            self.___url___, *args, **kwargs)


class Client(object):

    methods = ('GET', 'POST', 'PUT', 'DELETE')

    def __init__(self, host, headers=None, cookies=None, auth=None):
        """
        Client that provides an intuitive interface to building and 
        configuring requests. 
        :param host: the address (port included) of the API/resource. 
               e.g. 'someservice.com' or 'localhost:80'
        
        :param headers: Default headers that will be passed to all requests 
               unless explicitly changed with the 'set_headers' method. Any headers
               given as a parameter to the request, will be appended to the
               default headers, creating the headers for that particular request.
        
        :param cookies: Default cookies that will be passed to all requests unless
               explicitly changed with the 'set_cookies' method. Cookies are
               automatically merged into headers before each request. Must be
               dict with key value pairs. Any cookies given as a parameter to 
               the request, will be appended to the default and used as the
               cookies for that particular request.
        
        :param auth: requests-based Authentication object to use with each
               request. Can be overridden by passing a new auth object
               to the request
        """
        self.host = host
        self.cookies = {} if cookies is None else cookies
        self.headers = {} if headers is None else headers
        self.auth = auth

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

    def set_headers(self, headers):
        self.headers = headers

    def set_cookies(self, cookies):
        self.cookies = cookies

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

    def prepare_request(self, url, method):
        """

        :return: request object 
        """
        return self.bake_request(
            host=self.host, method=method, url=url,
            headers=self.headers, cookies=self.cookies,
            auth=self.auth
        )

    @staticmethod
    def bake_request(**kwargs):
        """
        Returns a Request instance prepared with **kwargs
        Can be overridden to support another Request type
        :param kwargs: Arguments for request object
        :return: Request Instance
        """
        return Request(**kwargs)

    def _start_build(self, method='GET'):
        request_obj = self.prepare_request('', method=method)
        return RequestBuilder('', request_obj)
