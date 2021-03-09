import unittest
from controllers.simple_data_source import SimpleDataSource
import datetime
import re

class TestSimpleDataSource(unittest.TestCase):
	"""
	Unit tests for DataSource.
	"""
	@classmethod
	def setUpClass(cls):
		cls.data_source = SimpleDataSource()

	def test_update_and_render(self):
		"""
		Description: Test if data source is able to update reqiured informations and generate correct content for output
		"""
		price = 1
		for i in range(5):
			now = datetime.datetime.now()
			self.data_source.update(now, price)
			formatted_content = self.data_source._format_content(now)
			price *= 2
			# no prev value at the beginning
			if i == 0:
				self.assertTrue(self.data_source.prev_cur_diff_percentage is None)
				self.assertRegex(
					formatted_content, 
					re.compile(
						'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d*\s+'
						'1\s+'
						'N/A\s+'
						'N/A\s+'
					)
				)
			if i > 0:
				self.assertTrue(self.data_source.prev_cur_diff_percentage == 1)
				self.assertRegex(
					formatted_content, 
					re.compile(
						'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d*\s+'
						'\d*\s+'
						'100.0%\s+'
						'N/A\s+'
					)
				)
			self.assertTrue(self.data_source.cur_yesterdaylast_diff_percentage is None)

		# test when price doesn't change
		now = datetime.datetime.now()
		self.data_source.update(now, price)
		self.data_source.update(now, price)
		formatted_content = self.data_source._format_content(now)
		self.assertTrue(self.data_source.prev_cur_diff_percentage == 0)
		self.assertRegex(
			formatted_content, 
			re.compile(
				'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d*\s+'
				'\d*\s+'
				'0.0%\s+'
				'N/A\s+'
			)
		)

	def test_update_yesterday_date(self):
		"""
		Description: Test if the value of 'Change between current scraped price and last yesterday’s last price expressed as percentage' is correctly updated each time
		"""
		self.data_source.update(datetime.datetime.now() + datetime.timedelta(days=1) , 64)
		self.assertTrue(self.data_source.cur_yesterdaylast_diff_percentage == 1 )

		self.data_source.update(datetime.datetime.now() + datetime.timedelta(days=1) , 128)
		self.assertTrue(self.data_source.cur_yesterdaylast_diff_percentage == 3 )

		self.data_source.update(datetime.datetime.now() + datetime.timedelta(days=2) , 128)
		self.assertTrue(self.data_source.cur_yesterdaylast_diff_percentage == 0 )

if __name__=="__main__":
	unittest.main()
