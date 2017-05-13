try:
    import requests
except:
    raise ImportError("requests package not found")


class RequestBuilder(object):

    def __init__(self, url, method):
        self.___url___ = url
        self.___md___ = method

    def __getattr__(self, name):
        url = '{}/{}'.format(self.___url___, name)
        return RequestBuilder(url, self.___md___)

    def __getitem__(self, item):
        return self.__getattr__(item)

    def __call__(self, **kwargs):
        return requests.request(self.___md___, self.___url___, **kwargs)


class Client(object):

    methods = ('GET', 'POST', 'PUT', 'DELETE')

    def __init__(self, host):
        """
        Client that provides an intuitive interface to building and 
        configuring requests. 
        :param host: the address (port included) of the API/resource. 
               e.g. 'someservice.com' or 'localhost:80'

        """
        self.host = host

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

    def change_base_url(self, url):
        self.host = url

    def _start_build(self, method):
        return RequestBuilder(self.host, method)
