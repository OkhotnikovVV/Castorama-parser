# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html


import scrapy

from itemloaders.processors import MapCompose, TakeFirst


def clear_price(value):
    if value:
        value = value.replace('\xa0', '')
        value = value.replace(' ', '')
        try:
            value = int(value)
        except:
            pass
        return value


def clear_name(name):
    if isinstance(name, str):
        return name.strip()
    return name


class CastoramaParserItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(input_processor=MapCompose(clear_name), output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(clear_price), output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field()
    _id = scrapy.Field()

