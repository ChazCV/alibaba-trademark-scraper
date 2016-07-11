import scrapy


class AliItem(scrapy.Item):
	"""Scrapy items are similar to python dictionaries and
	   are used for storing the scraped data.
	"""
	
    #Trademark searched.
    brand = scrapy.Field()
	
    #Number of alibaba.com listings returned.
    hits = scrapy.Field()
	
    #Yes if brand appears in the title of the first listing.
    in_title = scrapy.Field()
	
    #Category identification numbers for the first two related categories.
    rel_cat_1 = scrapy.Field()
    rel_cat_2 = scrapy.Field()

    #Number of listings for the first two related categories.
    rel_hits_1 = scrapy.Field()
    rel_hits_2 = scrapy.Field()

    #Yes if brand appears in the title of the related listings.
    rel_in_title_1 = scrapy.Field()
    rel_in_title_2 = scrapy.Field()
