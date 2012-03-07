# –*- encoding:utf8 –*-
import weibo
import db
from email.utils import parsedate_tz
from datetime import datetime

def formattime(t):
    t = parsedate_tz(t)
    t = datetime(t[0],t[1],t[2],t[3],t[4],t[5])
    return datetime.strftime(t, "%Y-%m-%d %H:%M:%S")


class MyDict():
    def __init__(self, d):
        self.d = d
    def __getattr__(self, attr):
        return self.d.get(attr, None)

def go():
    liwus = weibo.getLiwus()
    for liwu in liwus:
        liwu = MyDict(liwu)
        user = MyDict(liwu.user)
        if not liwu.thumbnail_pic or liwu.retweeted_status:
            continue
        try: 
            if db.Liwus.select(db.Liwus.c.ItemId==liwu.id).execute().fetchone():
                continue

            db.Liwus.insert().execute(ItemId=liwu.id, UserSinaUserId=user.id, Text=liwu.text, SinaUserName=user.name,
                CreateTime=formattime(liwu.created_at), ThumbnailPic=liwu.thumbnail_pic, BmiddlePic=liwu.bmiddle_pic, OriginalPc=liwu.original_pic,
                UserHeaderPic=user.profile_image_url, Hits=0, Sell=0, Recmmend=0) 
        except:
            if db.Liwus.select(db.Liwus.c.ItemId==liwu.id).execute().fetchone():
                continue

            db.Liwus.insert().execute(ItemId=liwu.id, UserSinaUserId=user.id, Text=liwu.text, SinaUserName=user.name,
                CreateTime=formattime(liwu.created_at), ThumbnailPic=liwu.thumbnail_pic, BmiddlePic=liwu.bmiddle_pic, OriginalPc=liwu.original_pic,
                UserHeaderPic=user.profile_image_url, Hits=0, Sell=0, Recmmend=0) 


