import scrapy
from ..items import RestaurantSpiderItem


class tripadviorSpider(scrapy.Spider):
    name = 'yelp'

    def __init__(self, *args, **kwargs):
        super(tripadviorSpider, self).__init__(*args, **kwargs)
        self.page_restaurant = 1

    def start_requests(self):

        # "https://www.yelp.com/search?cflt=restaurants&find_loc=Birmingham%2C+AL"
        # "https://www.yelp.com/city/birmingham-al#places-to-eat"

        yield scrapy.Request("", callback=self.parse)

    def parse(self, response):
        all_link = response.xpath()
        if all_link:
            for city in all_link:
                link = city.xpath("./a/@href").extract_first()
                if link:
                    link = response.urljoin(link)
                    yield scrapy.Request(url=link, callback=self.go_to_city)

    def go_to_city(self, response):
        link = response.xpath("//div[@class='biz-carousel restaurant-carousel']/h5/a/@href").extract_first()
        if link:
            link = response.urljoin(link)
            yield scrapy.Request(url=link, callback=self.scrape_city)

    def scrape_city(self, response):
        res = response.xpath(
            "//span[@class='lemon--span__373c0__3997G text__373c0__2Kxyz "
            "text-color--black-regular__373c0__2vGEn text-align--left__373c0__2XGa- "
            "text-weight--bold__373c0__1elNz text-size--inherit__373c0__2fB3p']")
        if res:
            for row in res:
                restaurant_url = row.xpath("./a/@href").extract_first()
                if restaurant_url:
                    restaurant_link = response.urljoin(restaurant_url)
                    yield scrapy.Request(url=restaurant_link, callback=self.scrape_sigle)  # meta={'item': items}

        next_page = response.xpath(
            "//a[@class='lemon--a__373c0__IEZFH link__373c0__1G70M next-link navigation-button__373c0__23BAT "
            "link-color--inherit__373c0__3dzpk link-size--inherit__373c0__1VFlE']/@href").extract()
        if next_page: # and self.page_restaurant < 1:
            next_page_link = response.urljoin(next_page[-1])
            yield scrapy.Request(url=next_page_link, callback=self.scrape_city)

        self.page_restaurant += 1

    def scrape_sigle(self, response):
        item = RestaurantSpiderItem()
        name = ''
        address = ''
        cuisine_type = ''
        price = ''
        location = ''
        name_ = response.xpath(
            "//h1[@class='lemon--h1__373c0__2ZHSL heading--h1__373c0__dvYgw undefined "
            "heading--inline__373c0__10ozy']/text()").extract_first()
        address_ = response.xpath(
            "//address[@class='lemon--address__373c0__2sPac']/p/span/text()").extract()  # address
        cuisine_type_ = response.xpath(
            "//span[@class='lemon--span__373c0__3997G display--inline__373c0__3JqBP margin-r1__373c0__zyKmV "
            "border-color--default__373c0__3-ifU']/span/a/text()").extract()
        price_ = response.xpath("//span[@class='lemon--span__373c0__3997G text__373c0__2Kxyz "
                                "text-color--normal__373c0__3xep9 text-align--left__373c0__2XGa- "
                                "text-bullet--after__373c0__3fS1Z text-size--large__373c0__3t60B']/text("
                                ")").extract_first()

        if address_:
            address = address_
            location = address_[-1]
        item['Location'] = location
        item['Address'] = address

        if name_:
            name = name_
        item['Restaurant'] = name

        if cuisine_type_:
            cuisine_type = cuisine_type_
        item['Cuisine_Type'] = cuisine_type

        if price_:
            price = price_
        item['Price'] = price

        yield item
