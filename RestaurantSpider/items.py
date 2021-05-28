# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RestaurantSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    Restaurant = scrapy.Field()
    Address = scrapy.Field()
    Cuisine_Type = scrapy.Field()
    Price = scrapy.Field()
    Location = scrapy.Field()
