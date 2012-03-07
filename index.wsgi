# –*- encoding:utf8 –*-
import os

import sae
import web
import config
import db
import fetchliwus

urls = (
    '/(\d*)',       'index',    #首页
    '/like/(\d*)',  'index',    #最受欢迎礼物
    '/new/(\d*)',   'New',      #最新礼物
    '/me/(\d*)',    'MyLike',   #最新礼物
    '/liwus',       'Liwus',    #fetch liwus
    '/show/(\d+)',  'ShowLiwu', #礼物详情页
    '/api/(\w+)',   'Api',      #json api
)

cfg = config.getconfig()

app_root = os.path.dirname(__file__)
templates_root = os.path.join(app_root, 'templates')
render = web.template.render(templates_root, base='layout')


def pageing(sql, page, pageSize=40):
    '把sqlalchemy的select语句进行分页'
    page = page and int(page) or 1
    page = page > 100 and 100 or page
    if page == 1:
        return sql.limit(pageSize)
    else:
        return sql.limit( pageSize ).offset( (page - 1) * pageSize)

def filter_liwu(liwus):
    '把缩略图替换成宽度为205的图片'
    for liwu in liwus:
        liwu = dict(liwu)

        liwu2 = {}
        for k, v in liwu.items():
            key = k.replace('Liwu_Likes_','')
            key = key.replace('Liwu_Items_','')
            liwu2[key] = v
        liwu = liwu2

        if liwu['Text'].find('http://t.cn/') != -1:
            continue

        liwu['ThumbnailPic'] = liwu['ThumbnailPic'].replace('/thumbnail/','/mw205/')
        yield liwu
def incrementHits(itemid):
    '递增喜欢数量'
    if not itemid:
        return 400
    db.Liwus.update().where(db.Liwus.c.ItemId==itemid).values(Hits=db.Liwus.c.Hits+1).execute()
    return 200

class index:
    '首页，最受欢迎礼物'
    def GET(self, page):
        liwus = pageing(db.Liwus.select().where(db.Liwus.c.Hits > 0)
            .order_by(db.Liwus.c.CreateTime.desc()), page).execute()
        return render.index(filter_liwu(liwus), 'like', cfg)

class New:
    '最新礼物'
    def GET(self, page):
        liwus = pageing(db.Liwus.select().order_by(db.Liwus.c.CreateTime.desc()), page).execute()
        return render.index(filter_liwu(liwus), 'new', cfg)

class MyLike:
    '我喜欢的礼物'
    def GET(self, page):
        sinaUserId = web.cookies().get('sinauserid')
        if not sinaUserId:
            return render.index([], 'mylike', cfg)
        liwus = pageing(db.Liwus.join(db.Likes, db.Liwus.c.ItemId == db.Likes.c.ItemId)
            .select(use_labels=True)
            .where(db.Liwus.c.Hits > 0 and db.Likes.c.UserSinaUserId == sinaUserId)
            .order_by(db.Liwus.c.CreateTime.desc()), page).execute()
        return render.index(filter_liwu(liwus), 'mylike', cfg)

class Liwus:
    '定时抓取礼物'
    def POST(self):
        web.header('Content-Type', 'text/html')
        fetchliwus.go()
        return '1'

class ShowLiwu:
    def GET(self, itemid):
        liwu = db.Liwus.select(db.Liwus.c.ItemId==itemid).execute().fetchone() 

        liwus = db.Liwus.select().where(db.Liwus.c.Hits > 0) \
            .order_by(db.Liwus.c.CreateTime.desc()).limit(12).execute()
        return render.show(liwu, filter_liwu(liwus), cfg) 

class Api:
    def GET(self, op):
        op = op.lower()
        web.header('Content-Type', 'text/html')
        data = web.input()
        if op == 'hits':
            itemid = data.itemid
            sinaUserId = web.cookies().get('sinauserid')
            if sinaUserId:
                db.Likes.insert().execute(SinaUserId=sinaUserId, ItemId=itemid)

            return incrementHits(itemid)
        elif op == 'nicai':
            db.Liwus.delete().where(db.Liwus.c.ItemId==data.itemid).execute()
            return 200

        return 404 

web.config.debug = True
app = web.application(urls, globals()).wsgifunc()

application = sae.create_wsgi_app(app)
