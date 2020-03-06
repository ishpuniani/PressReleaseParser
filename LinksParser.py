from lxml import html
import requests
from time import sleep
import json
from random import randint
import csv


def parse_finance_page(ticker):
    """
    Grab financial data from NASDAQ page

    Args:
      ticker (str): Stock symbol

    Returns:
      dict: Scraped data
    """
    key_stock_dict = {}
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-GB,en;q=0.9,en-US;q=0.8,ml;q=0.7",
        "Connection": "keep-alive",
        "Host": "www.nasdaq.com",
        "Referer": "http://www.nasdaq.com",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36"
    }

    base_url = 'http://www.nasdaq.com'

    # Retrying for failed request
    for retries in range(5):
        try:
            url = "http://www.nasdaq.com/market-activity/stocks/%s/press-releases" % (ticker)
            response = requests.get(url, headers=headers, verify=False)

            if response.status_code != 200:
                raise ValueError("Invalid Response Received From Webserver")

            print("Parsing %s" % (url))
            # Adding random delay
            sleep(randint(1, 3))
            parser = html.fromstring(response.text)

            pr_xpath = '//a[@class="quote-press-release__link"]/@href'

            links = parser.xpath(pr_xpath)
            print(links)

            new_links = []
            for link in links:
                nl = base_url + link
                new_links.append(nl)

            print(new_links)

            pr_data = {
                "ticker": ticker,
                "pr_links": new_links
            }
            return pr_data

        except Exception as e:
            print("Failed to process the request, Exception:%s" % (e))


if __name__ == "__main__":
    # argparser = argparse.ArgumentParser()
    # argparser.add_argument('ticker', help='Company stock symbol')
    # args = argparser.parse_args()

    ticker_file = 'NASDAQ-100_Tickers.csv'
    scraped_data = []
    with open(ticker_file, 'r', encoding='iso-8859-1') as tf:
        csv_reader = csv.reader(tf, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                ticker = row[1]
                print("Fetching data for %s" % (ticker))
                data = parse_finance_page(ticker)
                scraped_data.append(data)
                line_count += 1
        print(f'Processed {line_count} lines.')

    # ticker = 'amzn'
    # print("Fetching data for %s" % (ticker))
    # scraped_data = parse_finance_page(ticker)
    # print("Writing scraped data to output file")

    with open('links.json', 'w') as fp:
        json.dump(scraped_data, fp, indent=4, ensure_ascii=False)