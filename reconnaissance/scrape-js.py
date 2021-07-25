""" Scraping content loaded by JS using Selenium.

You need to install a browser and third-party browser
(or Web driver) for this script to work.
You can choose from Chrome, Firefox, Safari, or Edge.
We chose Chrome.

Install Chrome from https://www.google.com/chrome/
(and check version in its settings)

Install the chromedriver for that browser version:
$ wget https://chromedriver.storage.googleapis.com/index.html?path=87.0.4280.88/
$ unzip chromedriver_linux64.zip
$ sudo cp chromedriver /usr/bin/chromedriver
$ sudo chown root /usr/bin/chromedriver
$ sudo chmod +x /usr/bin/chromedriver
$ sudo chmod 755 /usr/bin/chromedriver

Test installation with:
$ chromedriver

There is a very common Google Chrome error when trying to
run it in Linux due to Chrome’s GPU usage.
Hence the --disable-gpu and --disable-software-rasterizer
options.

Authors: Reinica and Nina """

from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument("disable-gpu")
options.add_argument("disable-software-rasterizer")

browser = webdriver.Chrome('/usr/bin/chromedriver', options=options)

browser.get("https://tymyrddin.space")

result = browser.find_element_by_id("navbarCollapse")

print(result.text)
