# -*- coding: utf-8 -*-
import scrapy
from ..items import RrcItem
import datetime
import zmail
import logging

#  爬取汽车数据


class RrcSpider(scrapy.Spider):
    name = 'rrc'
    allowed_domains = ['www.renrenche.com']
    # start_urls = ['http://www.renrenche.com/']
    car_list = ['dazhong', 'fute', 'bieke', 'xiandai']
    city_list = ['bj', 'sh', 'zz', 'gz']
    time = datetime.datetime.now()
    custom_settings = {
        'ITEM_PIPELINES': {'RRC.pipelines.RrcPipeline': 300},
        # 生成日志文件
        'LOGIN_ENABLE': True,
        'LOG_ENCODING': 'UTF8',

        'LOG_FILE': '{}爬虫_{}年{}月{}日{}时{}分{}秒.log'.format(name, time.year, time.month,
                                                         time.day, time.hour,
                                                         time.minute, time.second),
        'LOG_LEVEL': 'INFO',
    }

    # 发送邮箱 ----------- 不想发送邮箱注释即可
    def __init__(self, send_user, root_code, receiver_user, log_file):
        super(RrcSpider, self).__init__()
        self.send_user = send_user
        self.root_code = root_code
        self.receiver_user = receiver_user
        self.log_file = self.name + log_file
        self.time = datetime.datetime.now()
        self.time_time = '{}年-{}月-{}日-{}时-{}分-{}秒'.format(self.time.year, self.time.month,
                                                          self.time.day, self.time.hour,self.time.minute, self.time.second)
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
    # -----------

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
        logging.info('汽车地址为：{}'.format(response.url))
        print(response.url)
        car = response.meta['car']
        title = response.xpath('//p[@class="detail-breadcrumb-tagP"]/a[last()]/text()').extract_first('')
        print(title)
        purchase_time = response.xpath('//li[@class="span7"]/div/p[2]/text()').extract_first('')
        mileage = response.xpath('//li[@class="kilometre"][1]/div/p[1]/strong/text()').extract_first('')
        money1 = response.xpath('//div[@class="list price-list"][1]/p/text()').extract_first('')
        money2 = response.xpath('//div[@class="list price-list"][1]/p/span/text()').extract_first('')
        money = money1 + money2
        down_payment = response.xpath('//div[@class="list payment-list"]/p[2]/text()').extract_first('')
        number_data = {
            '0': '0',
            '1': '1',
            '2': '2',
            '4': '3',
            '3': '4',
            '5': '5',
            '8': '6',
            '6': '7',
            '9': '8',
            '7': '9',
            '上': '上',
            '牌': '牌',
            '.': '.',
            '万': '万',
            '公': '公',
            '里': '里',
            '-': '-',
        }
        update_purchase_time = ''
        update_mileage = ''
        for x in purchase_time:
            update_purchase_time += number_data[x]
        for x in mileage:
            update_mileage += number_data[x]
        item = RrcItem()
        item['name'] = self.name
        item['title'] = title
        item['car'] = car
        item['update_purchase_time'] = purchase_time
        item['update_mileage'] = mileage
        item['money'] = money
        item['down_payment'] = down_payment
        yield item

    @staticmethod
    def close(spider, reason):
        mail_content = {
            'subject': '{}爬虫已关闭'.format(spider.name),
            'content': '{}爬虫关闭时间为：{}'.format(spider.name, spider.time_time),
            'attachments': spider.log_file

        }
        spider.sever_send_mail(spider.receiver_user, mail_content)
