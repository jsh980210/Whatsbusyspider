import scrapy
from ..items import RestaurantSpiderItem

class tripadviorSpider(scrapy.Spider):
    name = 'tripadvisor'

    def __init__(self, *args, **kwargs):
        super(tripadviorSpider, self).__init__(*args, **kwargs)
        self.page_restaurant = 1
        self.city_page = 1

    def start_requests(self):
        state_code = 28922
        end_code = 28973
        # "https://www.tripadvisor.com/Restaurants-g{0}".format(state_code) Alabama g28922
        # "https://www.tripadvisor.com/Restaurants-g28973-Wyoming.html" Wyoming g28973
        # "https://www.tripadvisor.com/Restaurants-g28953-New_York.html#LOCATION_LIST"
        while state_code <= end_code:
            yield scrapy.Request("https://www.tripadvisor.com/Restaurants-g{0}".format(state_code), callback=self.parse)
            state_code += 1

    def parse(self, response):
        count = 0

        if self.city_page == 1:
            for city in response.xpath("//div[@class='geo_name']"):
                #if count == 1:
                    #break
                city_url = city.xpath("./a/@href").extract_first()
                if city_url:
                    self.page_restaurant = 1
                    city_link = response.urljoin(city_url)
                    yield scrapy.Request(url=city_link, callback=self.scrape_city)
                count += 1
        else:
            for city in response.xpath("//ul[@class='geoList']/li"):
                #if count == 2:
                    #break
                city_url = city.xpath("./a/@href").extract_first()
                if city_url:
                    self.page_restaurant = 1
                    city_link = response.urljoin(city_url)
                    yield scrapy.Request(url=city_link, callback=self.scrape_city)
                count += 1

        next_page = response.xpath("//div[@class='unified pagination']/a/@href").extract()
        if next_page: # and self.page_restaurant < 1:
            self.city_page = 2
            next_page_link = response.urljoin(next_page[-1])
            yield scrapy.Request(url=next_page_link, callback=self.parse)


    def scrape_city(self, response):
        for row in response.xpath("//div[@class='_2Q7zqOgW']"):    # _2kbTRHSI # _2kbTRHSI  //div[@class='wQjYiB7z']/span/a/text()
            # skip sponsered
            if row.xpath("./div[@class='_2kbTRHSI']/div[@class='_1j22fice']"):
                continue

            restaurant_url = row.xpath("./div[@class='_2kbTRHSI']/div[@class='wQjYiB7z']/span/a/@href").extract_first()
            if restaurant_url:
                restaurant_link = response.urljoin(restaurant_url)
                yield scrapy.Request(url=restaurant_link, callback=self.scrape_sigle) # meta={'item': items}

        next_page = response.xpath("//div[@class='unified pagination js_pageLinks']/a/@href").extract()
        if next_page: # and self.page_restaurant < 1:
            next_page_link = response.urljoin(next_page[-1])
            yield scrapy.Request(url=next_page_link, callback=self.scrape_city)

        self.page_restaurant += 1

    def scrape_sigle(self, response):
        item = RestaurantSpiderItem()
        name = response.xpath("//h1[@class='restaurants-detail-top-info-TopInfo__restaurantName--1IKBe ui-header h1']/text()").extract_first()
        address = response.xpath("//a[@class='restaurants-detail-top-info-TopInfo__infoCellLink--2ZRPG']/text()").extract() # address
        cuisine_type = response.xpath("//a[@class='restaurants-detail-top-info-TopInfo__tagLink--2LkIo']/text()").extract()

        if address:
            item['Address'] = address[0]
            loc = address[0].split(',')
            item['Location'] = loc[-1].split()[0] + ' ' + loc[-1].split()[1] # .split('-')[0]

        if name:
            item['Restaurant'] = name

        if cuisine_type:
            price = cuisine_type[0]
            cuisine = cuisine_type[1:]
            if '$' not in price:
                price = ''
                cuisine = cuisine_type
            item['Price'] = price
            item['Cuisine_Type'] = cuisine

        yield item