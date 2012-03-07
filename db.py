# –*- encoding:utf8 –*-
import sae.const
from sqlalchemy import *
from sqlalchemy.pool import NullPool

dburl = 'mysql://%(user)s:%(pass)s@%(host)s:%(port)s/%(db)s' % \
    {
        'user' : sae.const.MYSQL_USER,
        'pass' : sae.const.MYSQL_PASS,
        'host' : sae.const.MYSQL_HOST,
        'port' : sae.const.MYSQL_PORT,
        'db' : sae.const.MYSQL_DB,
   }


db = create_engine(dburl, connect_args={'charset':'utf8'}, poolclass=NullPool)
metadata = MetaData(db)

Liwus = Table('Liwu_Items', metadata, autoload=True)
Likes = Table('Liwu_Likes', metadata, autoload=True)
