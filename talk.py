from __future__ import unicode_literals


from urlparse import urljoin
import requests


from scrapy.selector import Selector

from pprint import pprint


def fetch_page(url):

    r = requests.get(url)
    return r.text

def talk_links_from_listpage( url ):
    html = fetch_page( url )
    sel = Selector( text=html )
    talk_links = sel.css('.talk-link .media__message a::attr(href)').extract()
    return talk_links


def talk_from_page(url):
    html = fetch_page(url)
    sel = Selector(text=html)
    pprint( url )
    title = sel.css('.talk-hero__title').extract()
    description = sel.css('.talk-description').extract()
    pprint( title )
    pprint( description )
    return {
        'title' : title,
        'description' : description 
    }

def latest_talks(page=1):
    list_url = 'http://www.ted.com/talks/browse?page={0}'.format(page)
    talk_links = talk_links_from_listpage( list_url ) 
    talks = [talk_from_page('http://www.ted.com'+url) for url in talk_links]
    return talks

print("test")
pprint( latest_talks() )


