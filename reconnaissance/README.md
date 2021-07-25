# Scripts

## Data extraction

Requires the requests and beautifulsoup libraries

    $ pip3 install requests
    $ pip3 install beautifulsoup4

### Requests

The `GET` request is used to retrieve information from a web server (download the HTML content of a specified web page). Every request has a status code:

* 200: Indicates everything went OK and returns the result (if any)
* 301: Indicates the server is redirecting to a different endpoint
* 400: Indicates a bad request
* 401: Indicates we are not authenticated
* 403: Indicates trying to access forbidden resources
* 404: Indicates the resource is not available on the server

### Beatifulsoup

``beautifulsoup` is a Python library for web scraping (searching, navigating, and modifying).
