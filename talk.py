from __future__ import unicode_literals


from urlparse import urljoin
import requests


from scrapy.selector import Selector


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
    title = sel.css('.talk0-hero__title').extract()
    descripttion = sel.css('.talk-description').extract()
    return {
        'title' : title,
        'description' : description, 
    }

def latest_talks(page=1):
    list_url = 'http://www.ted.com/talks/browsers?page={0}''.format(Page)
    talk_links = talk_links_from_Listpage( list_url ) 
    talks = [talk_from_page(url) for url in talk_links]
    return talks


from pprint import pprint
pprint( latest_talks() )


