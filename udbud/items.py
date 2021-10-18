# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class UdbudItem(scrapy.Item):
    # define the fields for your item here like:
    tender_type = scrapy.Field()
    tender_title = scrapy.Field()
    contractor = scrapy.Field()
    place_of_delivery = scrapy.Field()
    announced_date = scrapy.Field()
    deadline_date = scrapy.Field()
    last_edited = scrapy.Field()
    document_type = scrapy.Field()
    description = scrapy.Field()
    tender_details = scrapy.Field()

    def __repr__(self):
        """Only print out tender name after exiting the Pipeline"""
        return repr({"tender_title": self["tender_title"]})
