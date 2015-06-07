# -*- coding: utf-8 -*-

import sys
import urllib
import urllib2
import logging
from bs4 import BeautifulSoup

def search(keyword, b=None):
    keyword_enc = urllib.quote(keyword)
    if b:
        url_string = "http://realtime.search.yahoo.co.jp/search?p=%s&b=%d" % (keyword, b)
    else:
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

    html = search('CYBR', 10)
    soup = BeautifulSoup(html)
    h2_soup = soup.find_all('h2')

    import pprint
    pprint.pprint(h2_soup)
