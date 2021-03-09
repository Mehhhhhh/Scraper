from requesters.nasdaq_requester import NasdaqRequester
import unittest
from unittest.mock import Mock, patch

class TestNasdaqRequester(unittest.TestCase):
	"""
	Unit tests for NasdaqRequester.
	"""
	def test_get_last_sale_price(self):
		"""
		Check if the function properly produces last sale price
		"""
		# mock reponse class to have different type of response
		class MockResponse:
			def __init__(self, json_data, is_ok):
				self.text = json_data
				self.ok = is_ok

			def json(self):
				return self.json_data

		#prepare side_effect for 3 possible cases, success, missing data in response and failed response.
		def mocked_requests_get_success(*args, **kwargs):
			return MockResponse('{"data": {"primaryData": {"lastSalePrice": "$250.1"}}}', True)
			
		def mocked_requests_get_missing_field(*args, **kwargs):
			return MockResponse('{"hello": "world"}', True)

		def mocked_requests_get_fail(*args, **kwargs):
			return MockResponse(None, False)
		
		# patch request
		with patch("nasdaq_requester.requests.get") as mock:
			nasdaq_requester = NasdaqRequester()
			mock.side_effect = mocked_requests_get_success
			self.assertTrue(nasdaq_requester.get_last_sale_price("fb") == 250.1)

			mock.side_effect = mocked_requests_get_missing_field
			self.assertTrue(nasdaq_requester.get_last_sale_price("fb") is None)

			mock.side_effect = mocked_requests_get_fail
			self.assertTrue(nasdaq_requester.get_last_sale_price("fb") is None)


if __name__=="__main__":
	unittest.main()