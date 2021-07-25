"""Web Crawler/Spider
This module implements a web crawler. This is very _basic_ only
and needs to be extended to do anything useful with the
traversed pages."""

import re
import sys
import time
import math
import urllib
import urllib.error
import urllib.request
from urllib.parse import urlparse
import optparse
from html import escape
from queue import Queue

from bs4 import BeautifulSoup

__version__ = "0.3"
USAGE = "%prog [options] <url>"
VERSION = "%prog v" + __version__

AGENT = "%s/%s" % (__name__, __version__)


class Link (object):

    def __init__(self, src, dst, link_type):
        self.src = src
        self.dst = dst
        self.link_type = link_type

    def __hash__(self):
        return hash((self.src, self.dst, self.link_type))

    def __eq__(self, other):
        return (self.src == other.src and
                self.dst == other.dst and
                self.link_type == other.link_type)
    
    def __str__(self):
        return self.src + " -> " + self.dst


class Crawler(object):

    def __init__(self, root, locked=True, filter_seen=True):
        self.root = root
        self.host = urlparse(root)[1]

        # Data for filters:
        self.locked = locked           # Limit search to a single host?

        self.urls_seen = set()          # Used to avoid putting duplicates in queue
        self.urls_remembered = set()    # For reporting to user
        self.visited_links = set()       # Used to avoid re-processing a page
        self.links_remembered = set()   # For reporting to user
        
        self.num_links = 0              # Links found (and not excluded by filters)
        self.num_followed = 0           # Links followed.  

        # Pre-visit filters:  Only visit a URL if it passes these tests
        self.pre_visit_filters = [self._not_visited, self._same_host]

        # Out-url filters: When examining a visited page, only process
        # links where the target matches these filters.        
        if filter_seen:
            self.out_url_filters = [self._same_host]
        else:
            self.out_url_filters = []

    def _pre_visit_url_condense(self, url):

        """ Reduce (condense) URLs into some canonical form before
        visiting.  All occurrences of equivalent URLs are treated as
        identical. (strip the "fragment" component from URLs) """

        base, frag = urllib.parse.urldefrag(url)
        return base

    """ URL Filtering functions using information from the state of the 
    Crawler. True indicates that the URL is to be used."""
    
    def _not_visited(self, url):
        """Pass if the URL has not already been visited"""
        return url not in self.visited_links
    
    def _same_host(self, url):
        """Pass if the URL is on the same host as the root URL"""
        try:
            host = urlparse(url)[1]
            return re.match(".*%s" % self.host, host) 
        except Exception as e:
            print(sys.stderr, "ERROR: Can't process url '%s' (%s)" % (url, e))
            return False

    def crawl(self):

        """ Main function in the crawling process.  Core algorithm is:
        q <- starting page
        while q not empty:
           url <- q.get()
           if url is new and suitable:
              page <- fetch(url)   
              q.put(urls found in page)
           else:
              nothing
        new and suitable means that we don't re-visit URLs we've seen
        already fetched, and user-supplied criteria like maximum
        search depth are checked. """
        
        q = Queue()
        q.put((self.root, 0))

        while not q.empty():
            this_url: object
            this_url, depth = q.get()

            # Apply URL-based filters.
            do_not_follow = [f for f in self.pre_visit_filters if not f(this_url)]
            
            # Special-case depth 0 (start URL)
            if depth == 0 and [] != do_not_follow:
                print(sys.stderr, "Whoops! Starting URL %s rejected by the following filters:", do_not_follow)

            # If no filters failed (that is, all passed), process URL
            if [] == do_not_follow:
                try:
                    self.visited_links.add(this_url)
                    self.num_followed += 1
                    page = Fetcher(this_url)
                    page.fetch()
                    for link_url in [self._pre_visit_url_condense(l) for l in page.out_links()]:
                        if link_url not in self.urls_seen:
                            q.put((link_url, depth+1))
                            self.urls_seen.add(link_url)
                            
                        do_not_remember = [f for f in self.out_url_filters if not f(link_url)]
                        if [] == do_not_remember:
                            self.num_links += 1
                            self.urls_remembered.add(link_url)
                            link = Link(this_url, link_url, "href")
                            if link not in self.links_remembered:
                                self.links_remembered.add(link)
                except Exception as e:
                    print(sys.stderr, "ERROR: Can't process url '%s' (%s)" % (this_url, e))
                    # print format_exc()


class OpaqueDataException (Exception):
    def __init__(self, message, mimetype, url):
        Exception.__init__(self, message)
        self.mimetype = mimetype
        self.url = url
        

class Fetcher(object):
    
    """The name Fetcher is a slight misnomer: This class retrieves and interprets web pages."""

    def __init__(self, url):
        self.url = url
        self.out_urls = []

    def __getitem__(self, x):
        return self.out_urls[x]

    def out_links(self):
        return self.out_urls

    def _addHeaders(self, request):
        request.add_header("User-Agent", AGENT)

    def _open(self):
        url = self.url
        try:
            request = urllib.request.Request(url)
            handle = urllib.request.build_opener()
        except IOError:
            return None
        return request, handle

    def fetch(self):
        request, handle = self._open()
        self._addHeaders(request)
        if handle:
            try:
                data = handle.open(request)
                mime_type = data.info().get_content_type()
                url = data.geturl()
                if mime_type != "text/html":
                    raise OpaqueDataException("Not interested in files of type %s" % mime_type,
                                              mime_type, url)
                content = data.read().decode("utf-8", errors="replace")
                soup = BeautifulSoup(content, "html.parser")
                tags = soup('a')
            except urllib.error.HTTPError as error:
                if error.code == 404:
                    print(sys.stderr, "ERROR: %s -> %s" % (error, error.url))
                else:
                    print(sys.stderr, "ERROR: %s" % error)
                tags = []
            except urllib.error.URLError as error:
                print(sys.stderr, "ERROR: %s" % error)
                tags = []
            except OpaqueDataException as error:
                print(sys.stderr, "Skipping %s, has type %s" % (error.url, error.mimetype))
                tags = []
            for tag in tags:
                href = tag.get("href")
                if href is not None:
                    url = urllib.parse.urljoin(self.url, escape(href))
                    if url not in self:
                        self.out_urls.append(url)


def getLinks(url):
    page = Fetcher(url)
    page.fetch()
    for i, url in enumerate(page):
        print("%d. %s" % (i, url))


def parse_options():
    """parse_options() -> opts, args
    Parse any command-line options given returning both
    the parsed options and arguments.
    """

    parser = optparse.OptionParser(usage=USAGE, version=VERSION)

    parser.add_option("-q", "--quiet", action="store_true", default=False, dest="quiet",
                      help="Enable quiet mode")

    parser.add_option("-l", "--links", action="store_true", default=False, dest="links",
                      help="Get links for specified url only")

    opts, args = parser.parse_args()

    if len(args) < 1:
        parser.print_help(sys.stderr)
        raise SystemExit(1)

    return opts, args
    

def main():    
    opts, args = parse_options()

    url = args[0]

    if opts.links:
        getLinks(url)
        raise SystemExit(0)

    sTime = time.time()
    print(sys.stderr,  "Crawling %s" % url)
    crawler = Crawler(url)
    crawler.crawl()

    eTime = time.time()
    tTime = eTime - sTime

    print(sys.stderr, "Found:    %d" % crawler.num_links)
    print(sys.stderr, "Followed: %d" % crawler.num_followed)
    print(sys.stderr, "Stats:    (%d/s after %0.2fs)" % (int(math.ceil(float(crawler.num_links) / tTime)), tTime))


if __name__ == "__main__":
    main()
