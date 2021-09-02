from scrapy import Request, Spider
from ..items import BookprojectItem


class BookSpider(Spider):
    name = 'book'
    custom_settings = {
        'DOWNLOAD_DELAY': 0.25,
        'CONCURRENT_REQUESTS': 8,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 8
    }

    def start_requests(self):
        url = 'https://www.quge7.com/book/1472'
        yield Request(url = url, callback = self.parse)

    def parse(self, response):
        # print(response.url)
        urls = response.xpath('//dd/a/@href').getall()
        urls = urls[:1]
        for url in urls:
            if url.find('/book/1472') >= 0:
                url = 'https://www.quge7.com' + url
                yield Request(url = url, callback = self.get_chapter_info)

    def get_chapter_info(self, response):
        title = response.xpath('//h1[@class="wap_none"]/text()').get()
        item = BookprojectItem()
        item['chapter_title'] = title
        chapter_id = response.url.split('/')
        chapter_id = chapter_id[len(chapter_id) - 1]
        chapter_id = chapter_id.split('.')[0]
        item['chapter_id'] = chapter_id
        item['chapter_content'] = response.xpath('//div[@id="chaptercontent"]/text()').getall()
        # print(item)
        yield item
