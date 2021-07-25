""" Scraping content using PhantomJS webdriver and Selenium.

To scrape a page that contains an iframe, scrape the iframe source.

Authors: Reinica and Nina """

from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup

try:
    html = urlopen("https://developer.mozilla.org/en-US/docs/Web/HTML/Element/iframe")
except HTTPError as err:
    print(err)
except URLError:
    print("Server down or incorrect domain")
else:
    # Read the returned HTML using the html.read() method and built-in parser
    soup = BeautifulSoup(html.read(), "html.parser")

    tag = soup.find("iframe")
    # URl of iframe ready for scraping
    print(tag['src'])
