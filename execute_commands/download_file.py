#!/usr/bin/env python3

import requests  # https://docs.python-requests.org/en/latest/


def download(url):
    get_response = requests.get(url)
    file_name = url.split("/")[-1]
    with open(file_name, "wb") as output_file:
        output_file.write(get_response.content)


download(
    "https://raw.githubusercontent.com/tymyrddin/darkest-forest/main/assets/images/warning.png"
)
