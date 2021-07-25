#!/usr/bin/python3



from urllib.request import Request, urlopen
from urllib.error import URLError

def get_html(url):
    # construct an http request for the given url 
    req = Request(url,
              data=None, 
              headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})

    # send request and fetch html
    html = None
    try:
        html = urlopen(req)
    except URLError as e:
        if hasattr(e, 'reason'):
            print('We failed to reach a server.')
            print('Reason: ', e.reason)
        elif hasattr(e, 'code'):
            print('The server couldn\'t fulfill the request.')
            print('Error code: ', e.code)

    # on error, simply return an empty binary string
    if html is None:
        print('Server not found')
        html = b''

    # on success, read the html content into a binary string
    else: 
        html  = html.read()

    return html



import requests
from bs4 import BeautifulSoup

page_result = requests.get('https://tymyrddin.space')
parse_object = BeautifulSoup(page_result.content, 'html.parser')

container = parse_object.find(class_='container')
container_p_content = container.find_all('p')

print(container_p_content)