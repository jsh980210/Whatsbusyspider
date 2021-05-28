import scrapy

class RestaurantSpider(scrapy.Spider):
    name = 'Restaurant'

    def __init__(self, restaurantName=None, *args, **kwargs):
        super(RestaurantSpider, self).__init__(*args, **kwargs)
        self.restaurantName = restaurantName
        self.switch = 0

    def start_requests(self):
        yield scrapy.Request('https://openmenu.com/find.php?r=%s' % self.restaurantName)

    def parse(self, response):
        if self.switch == 0:
            self.switch = 1
            location_url = response.xpath("//div[@class='small']/a/@href").extract_first()
            if location_url is not None:
                full_location_link = response.urljoin(location_url)
                yield scrapy.Request(url=full_location_link, callback=self.parse)
        else:
            for row in response.xpath("//div[@class='row spacer-sm']"):
                cuisine_type = row.xpath(".//div[@class='small']/text()").extract_first()
                cuisine_type = cuisine_type.split(':')[1].split('|')[0]
                yield {
                    'Restaurant': row.xpath(".//h4[@class='heading-primary']/a/strong/text()").extract_first(),
                    'Address': row.xpath(".//div[@class='text-muted']/text()").extract_first(),
                    'Segment': 'Segment',
                    'Sub-segment': 'Sub-segment',
                    'Cuisine Type': cuisine_type
                }
