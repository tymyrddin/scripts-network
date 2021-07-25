""" Scraping content using PhantomJS webdriver and Selenium.

PhantomJS loads a page and runs our selector code without opening any browsers.

Install PhantomJS:
$ sudo apt-get install build-essential chrpath libssl-dev libxft-dev
$ sudo apt-get install libfreetype6 libfreetype6-dev libfontconfig1 libfontconfig1-dev

Download the latest version from http://phantomjs.org/download.html
$ export PHANTOM_JS="phantomjs-2.1.1-linux-x86_64"
$ wget https://bitbucket.org/ariya/phantomjs/downloads/$PHANTOM_JS.tar.bz2
$ sudo tar xvjf $PHANTOM_JS.tar.bz2 -C /usr/local/share/
$ sudo ln -sf /usr/local/share/$PHANTOM_JS/bin/phantomjs /usr/local/bin

Test installation with:
$ phantomjs --version

There is a common error when trying to run it. The ‘libssl_conf.so’probably does not exist.
And the Phantom coders are overloaded. A workaround is running the command:
$ export OPENSSL_CONF=/etc/ssl/

The script will still work (for now) but with a UserWarning: Selenium support for PhantomJS
has been deprecated, please use headless versions of Chrome or Firefox instead.
Note that phantomJS will create a ghostdriver.login the directory where the script resides.
We will not be developing with this script further.

Authors: Reinica and Nina """

from selenium import webdriver

browser = webdriver.PhantomJS()

browser.get("https://tymyrddin.space")

print(browser.find_element_by_class_name("navbar").text)

browser.close()