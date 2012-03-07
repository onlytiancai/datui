#encoding=utf-8

fetch_keyword = u'美腿'
site_word = u'美腿'
site_name = u'晒美腿'
page_title = u'晒美腿 - 分享美腿，分享快乐'
weibo_api_key = 123456778 #这里改成你的api_key哦 

def getconfig():
    ret = globals()
    del ret['__builtins__']
    del ret['__name__']
    del ret['__doc__']
    return ret
