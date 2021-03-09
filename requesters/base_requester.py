from abc import ABC, abstractmethod

class BaseRequester(ABC):
    """
    Abstract base class for all requesters, this defines the interface of requests to get data.
    I suppose that in the future development, there might be plenty of different type of data we need, 
    they can be defined here to let concrete classes implement the details.
    """

    @abstractmethod
    def get_last_sale_price(self, company):
        """
        abstract method to get last sale's prices for a company

        :type company: str, company code that we want to get last sale price of
        :rtype: float/None, last sale's price
        """
        pass