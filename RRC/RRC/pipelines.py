# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
from scrapy.pipelines.images import ImagesPipeline
import scrapy


class RrcPipeline(object):
    def __init__(self, host, port, user, passwd, db, use_unicode, charset):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.db = db
        self.use_unicode = use_unicode
        self.charset = charset
        self.connect = MySQLdb.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            passwd=self.passwd,
            db=self.db,
            use_unicode=use_unicode,
            charset=self.charset,
        )
        self.cursor = self.connect.cursor()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(host=crawler.settings.get('HOST'),
                   port=crawler.settings.get('PORT'),
                   user=crawler.settings.get('USER'),
                   passwd=crawler.settings.get('PASSWD'),
                   db=crawler.settings.get('DB'),
                   use_unicode=crawler.settings.get('USE_UNICODE'),
                   charset=crawler.settings.get('CHARSET'),)

    def process_item(self, item, spider):
        insert_sql = "insert into {}" \
                     "(title, update_purchase_time, update_mileage, money, down_payment)" \
                     "values ('{}', '{}', '{}', '{}', '{}')"\
            .format(item['car'], item['title'], item['update_purchase_time'],
                    item['update_mileage'], item['money'], item['down_payment'])
        self.cursor.execute(insert_sql)
        self.connect.commit()
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()


class ImgPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        for x in item['src']:
            yield scrapy.Request(url=x, meta={'item': item})

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        title = item['title']
        src_name = item['src'][0].split('/')[-1]
        return '%s/%s' % (title, src_name)
