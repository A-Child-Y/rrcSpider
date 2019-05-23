# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RrcItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    car = scrapy.Field()
    title = scrapy.Field()
    update_purchase_time = scrapy.Field()
    update_mileage = scrapy.Field()
    money = scrapy.Field()
    down_payment = scrapy.Field()


class RrcIItem(scrapy.Item):
    name = scrapy.Field()
    src = scrapy.Field()
    title = scrapy.Field()
