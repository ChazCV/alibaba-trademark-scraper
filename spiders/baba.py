import re
import csv

from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy import optional_features

from alibaba.items import AliItem

 
class AliSpider(CrawlSpider):
    """Introduce a spider to perform the web crawling and data extraction
	using a list of URLs that act as the spider's starting point. A list
	of trademarks is given as the input file and each trademark is individually
	appended to alibaba.com's general search URL, an alibaba.com search is then
	performed on that specific trademark.
	"""
	
    name = "baba"
    allowed_domains = ['alibaba.com']   
    base_url = 'http://www.alibaba.com/trade/search?fsb=y&IndexArea=product_en&CatId=&SearchText='
    with open('trademarks.csv', 'r') as infile:
        reader = csv.reader(infile, delimiter=',', quotechar='"')
        for trademark in reader:
            trademark = trademark[0]
            url = base_url + trademark.strip()
            start_urls.append(url)
                        
    def parse(self, response):
		"""Crawl the indivudal brand (or trademark) results page for the 
		defined Scrapy items. The spider then follows the first two
		'Related Categories' links.
		"""
									
		sel = Selector(response)
		hits = sel.xpath('normalize-space(//div[@class="view-label"]/strong/text())').extract()
		brand = sel.xpath('//span[@id="J-m-search-text"]/input/@value').extract()[0]
		in_first_title = sel.xpath('/descendant::h2[@class="title"][1]/a/strong/text()').extract()[0]
		item = AliItem()          
		if in_first_title.lower() == brand.lower():
		   item['in_first_title'] = "True"                  
		else:
		   item['in_first_title'] = "False"              
		item['brand'] = brand
		item['hits'] = hits
		item['rel_cat_1'] = sel.xpath('//div[@class="item parent"]/a/@href').extract()[0]
		request = scrapy.Request(item['rel_cat_1'],
								 callback= self.parserel_cat_1)
		request.meta['item'] = item 
		yield request
		item['rel_cat_2'] = sel.xpath('//div[@class="item parent"]/a/@href').extract()[1]
		request = scrapy.Request(item['rel_cat_2'],
								 callback=self.parserel_cat_2, 
								 meta={'item': item})
		yield request
			   
    def parse_related_category_1(self, response):
		"""Similar to Parse. Crawl and extract the brand data for the 
		first related category.
		"""
		
		sel = Selector(response)
		item = response.meta['item']
		hits = sel.xpath('normalize-space(//div[@class="view-label"]/strong/text())').extract()
		item['rel_hits_1'] = rel_hits_1
		reg = response.request.url
		reg = re.search('F0\/([^\/]+)\/CID(\d+)', reg)
		rel_cat_1 = reg.group(2)
		item['rel_cat_1'] = rel_cat_1
		rel_in_title_1 = reg.group(1)
		in_first_title = sel.xpath('/descendant::h2[@class="title"][1]/a/strong/text()').extract()[0]
		if rel_in_title_1.lower() == in_first_title.lower():
			item['rel_in_title_1'] = "True"
		else:
			item['rel_in_title_1'] = "False"
		yield item

    def parse_related_category_2(self, response):
		"""Similar to Parse. Crawl and extract the brand data for the 
		second related category.
		"""
		
		sel = Selector(response)
		item = response.meta['item']
		hits = sel.xpath('normalize-space(//div[@class="view-label"]/strong/text())').extract()
		item['rel_hits_2'] = rel_hits_2
		reg = response.request.url
		reg = re.search('F0\/([^\/]+)\/CID(\d+)', reg)
		rel_cat_2 = reg.group(2)
		item['rel_cat_2'] = rel_cat_2
		rel_in_title_2 = reg.group(1)
		in_title = sel.xpath('/descendant::h2[@class="title"][1]/a/strong/text()').extract()[0]
		if rel_in_title_2.lower() == in_title.lower():
			item['rel_in_title_2'] = "True"
		else:
			item['rel_in_title_2'] = "False"             
		yield item
