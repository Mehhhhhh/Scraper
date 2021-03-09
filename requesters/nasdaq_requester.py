import logging
from requesters.base_requester import BaseRequester
import requests
import json

logger = logging.getLogger(__name__)

class NasdaqRequester(BaseRequester):
    """
    Concrete class that handles nasdaq data.
    """
    _request_url = "https://api.nasdaq.com/api/quote/{company}/info?assetclass=stocks"
    _header_path = "/api/quote/{company}/info?assetclass=stocks"
    _currency = "$"

    def __init__(self):
        """
        Constructor
        """
        self.session = requests.session()
        self.headers = {
            "authority": "api.nasdaq.com",
            "method": "GET",
            "scheme": "https",
            "accept": "application/json, text/plain, */*",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
            "origin": "https://www.nasdaq.com",
            "referer": "https://www.nasdaq.com/",
            "sec-ch-ua": '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
        }

    def get_last_sale_price(self, company):
        """
        Implement BaseRequester.get_last_sale_price, method to get last sale's price for nasdaq page.

        :type company: str, company code that we want to get last sale price of
        :rtype: float/None, last sale's price
        """
        logger.info(f"getting last sale price for {company}")

        self.headers["path"] = self._header_path.format(company=company)
        try:
            response = requests.get(self._request_url.format(company=company), headers=self.headers)
            if response.ok:
                logger.info(f"successfully get last sale price for {company}")
                return self._parse_response_text(response.text)
            else:
                logger.error("http response is KO")
                return None
        except:
            logger.error("unable to finish request")
            return None

    def _parse_response_text(self, response_text):
        """
        get last sale price from the response text

        :type response_text: str, text of https reponse body
        :rtype:float, float value of the last sale prince
        """
        response_json = json.loads(response_text)
        try:
            last_sale_price = float(response_json["data"]["primaryData"]["lastSalePrice"].split(self._currency)[1])
        except KeyError:
            last_sale_price = None
            logger.error("Unable to get last sale price from reponse text")
        return last_sale_price