import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import UunitedfidelityItem
from itemloaders.processors import TakeFirst

pattern = r'(\xa0)?'

class UunitedfidelitySpider(scrapy.Spider):
	name = 'unitedfidelity'
	start_urls = ['https://www.unitedfidelity.com/united-fidelity-bank-news/']

	def parse(self, response):
		post_links = response.xpath('//a[@class="slide-image"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		date = "Not stated in article"
		title = response.xpath('//h1/text()').get()
		if not title:
			title = response.xpath('//h2/text()| //h3/text()').get()
		content = response.xpath('//div[@class="avia_textblock  "]//text()[not (ancestor::h2)] |//div[@class="entry-content"]//text()').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))

		item = ItemLoader(item=UunitedfidelityItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()
