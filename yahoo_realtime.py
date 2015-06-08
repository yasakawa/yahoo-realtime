# -*- coding: utf-8 -*-

import sys
import re
import urllib
import urllib2
import logging
from bs4 import BeautifulSoup

def search(keyword):
    keyword_enc = urllib.quote(keyword)
    url_string = "http://realtime.search.yahoo.co.jp/search?p=%s&ei=UTF-8" % (keyword)
        
    useragent = "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko"
    logging.info("URL: %s" % url_string)
    try:
        req = urllib2.Request(url_string)
        req.add_header("User-agent", useragent)
        response = urllib2.urlopen(req)
        #response = urllib2.urlopen(url_string)
        logging.info("Finish downloading html.")
        retstr = response.read()
    except Exception, e:
        logging.error('type:' + str(type(e)))
        logging.error('args:' + str(e.args))
        logging.error('message:' + e.message)
        logging.error(str(e))
        return
    
    #print retstr
    return retstr


if __name__ == '__main__':
    argvs = sys.argv  # コマンドライン引数を格納したリストの取得
    argc = len(argvs) # 引数の個数

    reg = re.compile(r"http%3a//twitter.com/([A-Za-z0-9_]+)/status/([0-9]+)")

    html = search('CYBR')
    soup = BeautifulSoup(html)
    
    tweets = []
    
    cnf_soups = soup.find_all('div', class_="cnt" )
    for cnf_soup in cnf_soups:
        tweet = {}
        tweet['data_time'] = cnf_soup['data-time']

        h2_soup = cnf_soup.find('h2')
        tweet['text'] = h2_soup.get_text(strip=True)
        
        inf_soups = cnf_soup.select('a[title]')
        if inf_soups:
            href = inf_soups[0]['href']
            match = reg.search(href)            

            tweet['screen_name'] = match.group(1)
            tweet['tweet_id_str'] = match.group(2)
            tweets.append(tweet)
        
    import pprint
    pprint.pprint(tweets)
