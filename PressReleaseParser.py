from lxml import html
import requests
from time import sleep
import json
from random import randint
import os
import re


def parse_pr(url):
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

    # Retrying for failed request
    for retries in range(5):
        try:
            response = requests.get(url, headers=headers, verify=False)

            if response.status_code != 200:
                raise ValueError("Invalid Response Received From Webserver")

            print("Parsing %s" % (url))
            # Adding random delay
            sleep(randint(1, 3))
            parser = html.fromstring(response.text)

            title_xpath = '//h1[@class="press-release-header__title"]/text()'
            subtitle_xpath = '//h2[@class="press-release-header__subtitle"]/text()'
            date_xpath = '//time[@class="timestamp__date"]/text()'
            content_xpath = '//div[@class="body__content"]/p//text()'

            title = parser.xpath(title_xpath)
            title = ''.join(title)
            title = re.sub('\\n(\s*)', '', title)

            subtitle = parser.xpath(subtitle_xpath)
            subtitle = ''.join(subtitle)
            subtitle = re.sub('\\n(\s*)', '', subtitle)

            date = parser.xpath(date_xpath)
            date = ''.join(date)

            content = parser.xpath(content_xpath)
            content = ''.join(content)

            pr = {
                'title': title,
                'subtitle': subtitle,
                'date': date,
                'content': content
            }
            return pr

        except Exception as e:
            print("Failed to process the request, Exception:%s" % (e))


def download_pr(filename):
    with open(filename) as json_file:
        links = json.load(json_file)
        for obj in links:
            ticker = obj['ticker']
            pr_links = obj['pr_links']
            file_path = 'releases/%s_pr.json' % ticker
            press_releases = []
            if os.path.exists(file_path):
                print('PRs already downloaded for %s' % ticker)
            else:
                print('Downloading PRs for %s' % ticker)
                for link in pr_links:
                    pr = parse_pr(link)
                    press_releases.append(pr)

                print('Writing PRs for %s' % ticker)
                with open(file_path, 'w') as fp:
                    json.dump(press_releases, fp, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    '''
    Get press release content using links file
    Use links file
    Hit each link
    Get title, subtitle, date, content
    '''
    # download_pr('links.json')
    data = parse_pr('http://www.nasdaq.com/press-release/amazon-reveals-top-10-states-cities-and-top-categories-with-the-most-handmade-makers')
    print(data)
