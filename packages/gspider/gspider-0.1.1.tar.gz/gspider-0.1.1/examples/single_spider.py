# coding=utf-8

from gspider import Spider, HttpRequest, run_spider, Selector


class SingleSpider(Spider):
    def start_requests(self):
        yield HttpRequest("http://www.henan.gov.cn/zwgk/fgwj/yz/index.html")

    def parse(self, response):
        print('###', response)
        selector = Selector(response.text)
        content = selector.css("body").text
        print(content)


if __name__ == '__main__':
    run_spider(SingleSpider)
