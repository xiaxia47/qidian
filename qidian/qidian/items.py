# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QidianItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    author = scrapy.Field()
    book_id = scrapy.Field()
    book_type = scrapy.Field()
    book_sub_type = scrapy.Field()
    book_name = scrapy.Field()
    book_url = scrapy.Field()
    total_words = scrapy.Field()
    click_count = scrapy.Field()
    recommand_count = scrapy.Field()
    book_status = scrapy.Field()
    rank_score = scrapy.Field()
    rank_ppl_involved = scrapy.Field()
    last_upload_date = scrapy.Field()
    

