import scrapy
import re

from chuangyepudata.items import InvestEvent

class InvestEventSpider(scrapy.Spider):
	name = "investevent"
	allowed_domains = ['chuangyepu.com']
	start_urls = ['http://chuangyepu.com/investments/page/%s' % page for page in xrange(1, 660)]

	def parse(self, response):
		for sel in response.xpath('//div[contains(@class, "public_wrapper")]/div[contains(@class, "col-xs-12")]/table//tr/td[2]'):
			item = InvestEvent()
			item['url'] = sel.xpath('div[1]/a/@href').extract()
			item['company'] = sel.xpath('div[1]/a/text()').extract()
			if not item['company']:
				item['company'] = sel.xpath('div[1]/text()').extract()
			item['date'] = sel.xpath('p[1]/text()').extract()
			item['phase'] = sel.xpath('p[1]/text()').extract()
			item['money'] = sel.xpath('p[1]/strong/text()').extract()
			item['description'] = sel.xpath('div[@class="desc"]/p/text()').extract()
			item['description'] = ' '.join(item['description'])
			item['description'] = re.sub(u'\r\n', '', item['description']).replace('\n', '')
			item['institutions'] = sel.xpath('div[@class="invest-detail"]/span/small/a/text()').extract()
			yield item