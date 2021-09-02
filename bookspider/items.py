# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookprojectItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    chapter_id = scrapy.Field()
    chapter_title = scrapy.Field()
    chapter_content = scrapy.Field()
    pass
