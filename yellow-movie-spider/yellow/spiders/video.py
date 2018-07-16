import scrapy
from yellow.items import YellowItem

class VideoSpider(scrapy.Spider):
    name = "videos"
    domain = "https://www.9886e.com/"
    videos = []

    def start_requests(self):
        url = "https://www.9886e.com/Html/88/index-{}.html"

        # 从第二页开始
        for i in range(2, 32):
            u = url.format(i)
            yield scrapy.Request(url=u,callback=self.parse)

    def parse(self, response):
        urls = []
        for li in response.css("div.box.movie_list ul li"):
            urls.append(li.css("a::attr(href)").extract_first())

        # 再次针对url进行抓取
        for url in urls:
            yield scrapy.Request(url=self.domain + url,callback=self.parseDetail)

    def parseDetail(self, response):

        # 当前页面的视频地址
        item = YellowItem()
        item["url"] = response.css("ul.downurl font::text").extract_first()
        item["title"] = response.css(".film_title h1::text").extract_first()
        item["img"] = response.css(".movie_info img::attr(src)").extract_first()

        yield item
