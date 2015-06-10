# -*- coding: utf-8 -*-

import sys
import re
import urllib
import urllib2
import logging
from bs4 import BeautifulSoup

def search(keyword, useragent=None):
    """ Yahooリアルタイムからkeywordで検索する
    
    return sample
    [
     {'data_time': u'143305000',
      'screen_name': u'username',
      'text': u'ツイート本文',
      'tweet_id_str': u'123456789012345678',
      'ref':'Twitter'}, # Twitter or Facebook
      ...
    ]
    """
    keyword_enc = urllib.quote(keyword)
    url_string = "http://realtime.search.yahoo.co.jp/search?p=%s&ei=UTF-8" % (keyword)    
    try:
        req = urllib2.Request(url_string)
        if useragent:
            req.add_header("User-agent", useragent)
        response = urllib2.urlopen(req)
        html = response.read()
    except Exception, e:
        logging.error('type:' + str(type(e)))
        logging.error('args:' + str(e.args))
        logging.error('message:' + e.message)
        return
    
    return parse_html(html)


def pagenation(keyword, uts, useragent=None):
    """ Yahooリアルタイムからkeywordで検索する（ページング処理）
        uts: 前回の検索結果のUNIXタイム。これより古いツイートが返される """

    keyword_enc = urllib.quote(keyword)
    url_string = "http://realtime.search.yahoo.co.jp/paginationjs?p=%s&uts=%s" % (keyword, uts)
    try:
        req = urllib2.Request(url_string)
        if useragent:
            req.add_header("User-agent", useragent)
        response = urllib2.urlopen(req)
        html = response.read()
    except Exception, e:
        logging.error('type:' + str(type(e)))
        logging.error('args:' + str(e.args))
        logging.error('message:' + e.message)
        return
    
    return parse_html(html)
    

def parse_html(html):
    """ Yahooリアルタイムから返されたHTMLを解析する """

    tweets = []
    reg = re.compile(r"http%3a//twitter.com/([A-Za-z0-9_]+)/status/([0-9]+)")
    soup = BeautifulSoup(html)
    
    cnf_soups = soup.find_all('div', class_="cnt" )
    for cnf_soup in cnf_soups:
        tweet = {}
        tweet['data_time'] = cnf_soup['data-time']

        h2_soup = cnf_soup.find('h2')
        tweet['text'] = h2_soup.get_text(strip=True)

        ref_soup = cnf_soup.find('span', class_='ref')
        tweet['ref'] = ref_soup.get_text(strip=True)
        
        inf_soups = cnf_soup.select('a[title]')
        if inf_soups:
            href = inf_soups[0]['href']
            match = reg.search(href)

            tweet['screen_name'] = match.group(1)
            tweet['tweet_id_str'] = match.group(2)
            tweets.append(tweet)
    
    return tweets


if __name__ == '__main__':
    argvs = sys.argv  # コマンドライン引数を格納したリストの取得
    argc = len(argvs) # 引数の個数

    keyword = 'CYBR'
    useragent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko'

    tweets = search('CYBR', useragent)
    
    import pprint
    pprint.pprint(tweets)
    print("====================================================================")

    if len(tweets) == 10:
        last_uts = tweets[9]['data_time']
        tweets = pagenation(keyword, last_uts)

        import pprint
        pprint.pprint(tweets)
