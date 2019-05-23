# -*- coding: utf-8 -*-
import scrapy
from ..items import RrcIItem
import datetime
import zmail

# 爬取汽车的图片


class RrcSpider(scrapy.Spider):
    name = 'rrci'
    allowed_domains = ['www.renrenche.com']
    # start_urls = ['http://www.renrenche.com/']
    car_list = ['dazhong', 'fute', 'bieke', 'xiandai']
    city_list = ['bj', 'sh', 'zz', 'gz']
    time = datetime.datetime.now()
    custom_settings = {
        'ITEM_PIPELINES': {'RRC.pipelines.ImgPipeline': 300},
        # 本地图片保存文件
        'IMAGES_STORE': 'images',

        # 生成日志文件
        'LOGIN_ENABLE': True,
        'LOG_ENCODING': 'UTF8',

        'LOG_FILE': '{}爬虫_{}年{}月{}日{}时{}分{}秒.log'.format(name, time.year, time.month,
                                                         time.day, time.hour,
                                                         time.minute, time.second),
        'LOG_LEVEL': 'INFO',
    }

    #  发送邮件，可选配置-----------，注释不影响代码
    def __init__(self, send_user, root_code, receiver_user, log_file):
        super(RrcSpider, self).__init__()
        self.send_user = send_user
        self.root_code = root_code
        self.receiver_user = receiver_user
        self.log_file = self.name + log_file
        self.time = datetime.datetime.now()
        self.time_time = '{}年-{}月-{}日-{}时-{}分-{}秒'.format(self.time.year, self.time.month,
                                                          self.time.day, self.time.hour, self.time.minute,
                                                          self.time.second)
        self.server = zmail.server(self.send_user, self.root_code)
        self.mail_content = {
            'subject': '{}已开启了'.format(self.name),
            'content': '{}开始时间为：{}'.format(self.name, self.time_time)
        }
        self.server.send_mail(self.receiver_user, self.mail_content)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = cls(send_user=crawler.settings.get('SEND_USER'),
                     root_code=crawler.settings.get('ROOT_CODE'),
                     receiver_user=crawler.settings.get('RECEIVER_USER'),
                     log_file=crawler.settings.get('LOG_FILE'))
        spider.set_crawler(crawler)
        return spider
    # -------------------

    def start_requests(self):
        for city in self.city_list:
            for car in self.car_list:
                url = 'https://www.renrenche.com/{}/{}/p1/'.format(city, car)
                yield scrapy.Request(url=url, dont_filter=True, callback=self.parse, meta={'car': car})

    def parse(self, response):
        li_list = response.xpath('//ul[@class="row-fluid list-row js-car-list"]/li')
        for li in li_list:
            href = li.xpath('a[@class="thumbnail"]/@href').extract_first('')
            if href.startswith('/car'):
                del href
            elif href == "":
                del href
            else:
                info_url = 'https://www.renrenche.com' + href
                yield scrapy.Request(url=info_url, dont_filter=True, meta=response.meta, callback=self.get_data)

    def get_data(self, response):
        title = response.xpath('//p[@class="detail-breadcrumb-tagP"]/a[last()]/text()').extract_first('')
        li_list = response.xpath('//div[@class="thumb"]/ul/li')
        for li in li_list:
            item = RrcIItem()
            item['name'] = self.name
            item['title'] = title
            src = 'http:' + li.xpath('a/img/@src').extract_first('').split('?')[0]
            item['src'] = [src]
            print(src)
            yield item

    @staticmethod
    def close(spider, reason):
        mail_content = {
            'subject': '{}爬虫已关闭'.format(spider.name),
            'content': '{}爬虫关闭时间为：{}'.format(spider.name, spider.time_time),
            'attachments': spider.log_file
        }
        spider.sever_send_mail(spider.receiver_user, mail_content)

