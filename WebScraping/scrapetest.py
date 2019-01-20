from urllib2 import urlopen, HTTPError, URLError
from bs4 import BeautifulSoup
def getTitle(url):
    try:
        html = urlopen(url)
    except (HTTPError, URLError) as e:
        print e
        return None
    try:
        bsObj = BeautifulSoup(html.read(), 'lxml')
        title = bsObj.body.h1
    except AttributeError as e:
        print e
        return None
    return title
title = getTitle('http://pythonscraping.com/pages/page1.html')
if title:
    print title
raw_input("Press ENTER to exit")
print "Closing..."