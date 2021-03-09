# Scraper program

Simple scraper program that scrapes data from https://www.nasdaq.com/market-activity/stocks/fb and produce relevant information then output.
 
## Code Hierarchy
```{bash}
.  
|-- setenv  
|-- README.md  
|-- controllers  
|   |-- simple_data_source.py  
|   \`-- simple_data_source_test.py  
|-- logging.conf  
|-- main.py  
|-- output_handlers  
|   |-- base_handler.py  
|   |-- file_handler.py  
|   |-- output_handler_factory.py  
|   \`-- stdout_handler.py  
|-- requesters  
|   |-- base_requester.py  
|   |-- nasdaq_requester.py  
|   |-- nasdaq_requester_test.py  
|   \`-- requester_factory.py  
\`-- requirements.txt  
```

## Environment set-up
```{bash}
source setenv
```

## Execution examples

Use console
```{bash}
python scraper.py --scraping-interval-seconds 1 --output-mode console
```

Use file
```{bash}
python scraper.py --scraping-interval-seconds 1 --output-mode file --file-path ./out.a
```

## Genenral idea

The program could have been written in a monolithic way with a single function that does the minimum.
However it's worthwhile to make it more scalable for potential extension.

### Requesters

Requester is the layer for getting data from specified resources. There are:
- `BaseRequester` - Base class that defines the interfaces (in this case - getting the last sale price);
- `NasdaqRequester` - Concrete class that implements the underlying details;
> **Implementation for nasdaq webpage**
>
>The last sale's price is dynamically updated, therefore it's not possible to simply get the static html and fetch the data.  
>According to the network history from browser, calls to this API https://api.nasdaq.com/api/quote/FB/info?assetclass=stocks
> actually return useful information and then last sale's price can be found in the response body.

- `RequesterFactory` - Factory to get desired concrete requester class.


*Future considerations*
- new pages to parse -> new concrete requester class
- new data to get -> new interface in the base class and for each requesters to implement the details


### Controllers

Controller is in charge of managing and post-processing the scraped data. For this use case, a simple algorithm (we need only 4 variables that hold previous price, current price, date of today and yesterday's last price) can produce the required values:

-	Date and time of scraping
-	Last sale’s price
-	Change between last scraped price and current scraped price expressed as percentage
-	Change between current scraped price and last yesterday’s last price expressed as percentage

Afterwards, controllers let `output_handler` perform the outputting

*Future considerations*

- new data to calculate -> introduce new data structure/algorithm.
- new usage of data -> create new interface.

### Output handlers

There is a base class that defines the output() function to implement. Concrete classes are implemented as context manager since usually there are preparation and finalization during I/O. Concrete classes `file_handler` and `stdout_handler` work for file output and console output respectively.

*Future considerations*

- new way to output, for example output to db -> add new output handler and implement db manipulations
- Growing file size -> The logging module's RotatingFileHandler helps to keep the file at a 
constant size. 


