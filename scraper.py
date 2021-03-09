from requesters.requester_factory import RequesterFactory
from output_handlers.output_handler_factory import OutputHandlerFactory
from controllers.simple_data_source import SimpleDataSource

import time
import datetime
import argparse
import logging
import logging.config
import os

def run(interval, mode, file_path):
    """
    main execution, constant string can be configured somewhere else
    """
    with OutputHandlerFactory.get_output_handler(mode)(file_path) as output_handler:
        requester = RequesterFactory.get_requester("nasdaq")()
        fb_data_source = SimpleDataSource()
        while True:
            now = datetime.datetime.now()
            last_sale_price = requester.get_last_sale_price("fb")
            fb_data_source.update(now, last_sale_price)
            fb_data_source.render(now, output_handler)
            time.sleep(interval)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Simple Scraper")
    parser.add_argument('--scraping-interval-seconds', dest='interval', required=True, help="the interval of scraping in second")
    parser.add_argument('--output-mode', dest='output_mode', choices=['file', 'console'], required=True, help="the way to output scraped results")
    parser.add_argument('--file-path', dest='file_path', help="Path of the file that we want to store output into")
    args = parser.parse_args()

    if args.output_mode == "file":
        assert args.file_path, "You have chosen file output mode, you need to provide a file path using --file-path"

    fileDirectory = os.path.dirname(os.path.abspath(__file__))

    # Initialize logging, load config
    logging.config.fileConfig(os.path.join(fileDirectory, "logging.conf"), disable_existing_loggers=False)
    logger = logging.getLogger("Main")

    run(int(args.interval), args.output_mode, args.file_path)