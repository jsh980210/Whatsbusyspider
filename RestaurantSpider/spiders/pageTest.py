import scrapy

class pageSpider(scrapy.Spider):
    name = 'page'

    def __init__(self, restaurantName=None, *args, **kwargs):
        super(pageSpider, self).__init__(*args, **kwargs)
        self.restaurantName = restaurantName
        #self.items = RestaurantSpiderItem()
        self.items = {}

    def start_requests(self):
        yield scrapy.Request("https://www.tripadvisor.com/Restaurant_Review-g60763-d3263717-Reviews-Obao-New_York_City_New_York.html")

    def parse(self, response):
        address = response.xpath("//a[@class='restaurants-detail-top-info-TopInfo__infoCellLink--2ZRPG']/text()").extract()
        self.items['address'] = address[0]
        yield self.items
