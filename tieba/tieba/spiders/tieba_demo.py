import scrapy
from scrapy import Request
from ..items import TiebaItem
from scrapy_redis.spiders import RedisSpider

class TiebaDemoSpider(RedisSpider):
    name = 'tieba_demo'
    allowed_domains = ['cnblogs.com']
    # start_urls = ['https://news.cnblogs.com/']
    base_url = 'https://news.cnblogs.com'
    redis_key = "tieba:starturl"
    def parse(self, response):
        urls = response.xpath('//div[@class="news_block"]//h2/a/@href').getall()
        for url in urls:
            detail_url = self.base_url + url
            yield Request(url=detail_url,callback=self.parse_detail)

        next_url = self.base_url + response.xpath('//div[@class="pager"]/a[last()]/@href').get()
        if not next_url:
            return
        else:
            yield Request(next_url,callback=self.parse)

    def parse_detail(self,response):
        title = response.xpath('//div[@id="news_title"]/a/text()').get().strip()
        content = response.xpath('//div[@id="news_body"]/p/text()').getall()
        content = "".join(content).strip()
        item = TiebaItem(title=title,content=content)
        yield item
