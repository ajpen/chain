import unittest
import responses
import chain
import json


class TestChainClient(unittest.TestCase):

    def setUp(self):
        self.client = chain.Client('http://sample.com')

    def test_url_building(self):
        url1 = self.client.get.tea.cookies
        self.assertEqual("http://sample.com/tea/cookies", url1.___url___)

    def test_methods(self):

        url1 = self.client.get.tea.cookies

        self.assertEqual(
            "GET",
            url1.___md___,
            "Method did not equal GET but request was client.get"
        )

        url2 = self.client.post.bill.cash

        self.assertEqual(
            "POST",
            url2.___md___,
            "Method did not equal POST but request was client.post"
        )

        url3 = self.client.put.food.cake

        self.assertEqual(
            "PUT",
            url3.___md___,
            "Method did not equal PUT but request was client.put"
        )

        url4 = self.client.delete.drink.milk

        self.assertEqual(
            "DELETE",
            url4.___md___,
            "Method did not equal DELETE but request was client.delete"
        )


class TestChainRequest(unittest.TestCase):

    def setUp(self):
        self.client = chain.Client('http://sample.com')

    def tearDown(self):
        pass

    @responses.activate
    def test_get_request(self):
        responses.add(responses.GET, 'http://sample.com/tea/cookies',
                      json={"cookie": "Chocolate-Chip"}, status=200)

        expected_response = {'cookie': 'Chocolate-Chip'}
        response = self.client.get.tea.cookies()

        self.assertEqual(
            response.json(),
            expected_response,
            "Response body does not match expected"
        )

    @responses.activate
    def test_post_request(self):
        responses.add(responses.POST, 'http://sample.com/tea/cookies',
                      json={"cookie": "Chocolate-Chip"}, status=200)

        expected_response = {'cookie': 'Chocolate-Chip'}
        response = self.client.post.tea.cookies(
            json={'want': 'Chocolate-Chip'})

        self.assertEqual(
            response.json(),
            expected_response,
            "Response body does not match expected"
        )

        self.assertEqual(
            response.status_code, 200, "Status does not match expected")

        self.assertEqual(
            responses.calls[0].request.body.decode('utf-8'),
            json.dumps({"want": "Chocolate-Chip"}),
            "Request body does not match expected"
        )

    @responses.activate
    def test_numbers(self):
        responses.add(responses.GET, 'http://sample.com/tea/cookies/1',
                      json={"cookie": "Chocolate-Chip"}, status=200)

        expected_response = {'cookie': 'Chocolate-Chip'}
        response = self.client.get.tea.cookies[1]()

        self.assertEqual(
            response.json(),
            expected_response,
            "Response body does not match expected"
        )

    @responses.activate
    def test_special_chars(self):
        responses.add(responses.GET, 'http://sample.com/tea/cookies/$*',
                      json={"cookie": "Chocolate-Chip"}, status=200)

        expected_response = {'cookie': 'Chocolate-Chip'}
        response = self.client.get.tea.cookies["$*"]()

        self.assertEqual(
            response.json(),
            expected_response,
            "Response body does not match expected"
        )