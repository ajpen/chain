import requests
from chain.http_objects import Request


class RequestsRequest(Request):

    def send(self, url, query=None, body=None, headers=None, cookies=None,
             **kwargs):

        self.url = url if url is not None else self.url
        self.body = body if body is not None else self.body
        self.query = query if query is not None else self.query

        if headers:
            self.headers.update(headers)

        if cookies:
            self.cookies.update(cookies)

        self.build_url(self.query)
        return self.send_request(
            headers=self.headers, cookies=self.cookies,
            data=self.body, params=self.query, **kwargs
        )

    def build_url(self, query):
        # support the requests.Request url
        self.url = '{}{}'.format(self.host, self.url)

        super(RequestsRequest, self).build_url(query)

    def send_request(self, **kwargs):
        return requests.request(self.method, self.url, **kwargs)