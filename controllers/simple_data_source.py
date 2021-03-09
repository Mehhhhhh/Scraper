import datetime
import logging

logger = logging.getLogger(__name__)

class SimpleDataSource:
    """
    Data strcuture that holds required information 
    """

    def __init__(self, cur_sale_price=None, prev_sale_price=None, today=datetime.date.today(), yesterday_last_price=None):
        """
        Constructor, initializing vairiables

        :type cur_sale_price: float, the current fetched price
        :type prev_sale_price: float, the previously fetched price
        :type today: date, the date of today, private attribute to help determine yesterday_last_price 
        :type yesterday_last_price: float, the yesterday's last price
        """
        self.cur_sale_price = cur_sale_price
        self.prev_sale_price = prev_sale_price
        self._today = today
        self.yesterday_last_price = yesterday_last_price

    def update(self, time, last_sale_price):
        """
        Function to update the data

        :type last_sale_price: float, the new cur_price we want to update
        :type time: datetime, date and time that the new current price is fetched.
        """
        logger.info("updating data")
        # check if now is new day
        if (time.date() - self._today).days > 0:
            self._today = time.date()
            # if now is a new day, before updating self.cur_sale_price, set yesterday's last price as self.cur_sale_price (which represent yesterday's last value) 
            self.yesterday_last_price = self.cur_sale_price

        self.prev_sale_price, self.cur_sale_price = self.cur_sale_price, last_sale_price
        self.prev_cur_diff_percentage = (self.cur_sale_price - self.prev_sale_price)/self.prev_sale_price if self.prev_sale_price else None
        self.cur_yesterdaylast_diff_percentage = (self.cur_sale_price - self.yesterday_last_price)/self.yesterday_last_price if self.yesterday_last_price else None

    def render(self, date_time, output_handler):
        """
        Rendering the data source into output

        :type date_time: datetime, the date and time of current scraping
        :type output_handler: derived handler from BaseHandler, handling the output content.
        """
        output_handler.output(self._format_content(date_time))
    
    def _format_content(self, date_time):
        return "{date_time}\t{cur_sale_price}\t{prev_cur_diff_percentage}\t{cur_yesterdaylast_diff_percentage}\n".format(
                    date_time=date_time,
                    cur_sale_price=self.cur_sale_price if self.cur_sale_price is not None else "N/A",
                    prev_cur_diff_percentage=str(round(self.prev_cur_diff_percentage*100, 5)) + "%" if self.prev_cur_diff_percentage is not None else "N/A",
                    cur_yesterdaylast_diff_percentage=str(self.cur_yesterdaylast_diff_percentage*100) + "%" if self.cur_yesterdaylast_diff_percentage is not None else "N/A"
                )