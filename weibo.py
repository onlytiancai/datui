# –*- encoding:utf8 –*-
import urllib2
import json
import config

appkey = config.weibo_api_key 
url = 'http://api.t.sina.com.cn/trends/statuses.json?source=%s&trend_name=%s' % (appkey, config.fetch_keyword)
url=url.encode('utf-8')
url=urllib2.unquote(url)

def getLiwus():
    f = urllib2.urlopen(url)
    rsp = f.read()
    return json.loads(rsp)

