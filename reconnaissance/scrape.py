"""Scraping tags by using the urlopen library to connect to a web page, turning
the returned HTML into a Beautiful Soup object to extract HTML elements
by its surrounding tags."""

from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup


try:
    # Connect to page
    html = urlopen("https://tymyrddin.space")
except HTTPError as err:
    print(err)
except URLError:
    print("Server down or incorrect domain")
else:
    # Read the returned HTML using the html.read() method and built-in parser
    soup = BeautifulSoup(html.read(), "html.parser")

    tags = soup.findAll("title")
    for tag in tags:
        print(tag.getText())
