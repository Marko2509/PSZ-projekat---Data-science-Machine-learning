import scrapy
import os

# scrapy crawl cars -O cars.json

class CarsSpider(scrapy.Spider):
    name = "cars"

    start_urls = [
        'https://www.polovniautomobili.com/auto-oglasi/pretraga?brand=&price_to=&year_from=&year_to=&showOldNew=all&submit_1=&without_price=1'
    ]

    curr_num_of_cars = 0
    MAX_NUM_OF_CARS = 25000

    def parse(self, response):
        car_page = response.css('h2 > a.ga-title')
        yield from response.follow_all(car_page, callback = self.parse_car)

        next_page = response.css('a.js-pagination-next:nth-of-type(1)')
        yield from response.follow_all(next_page, callback = self.parse)

    def parse_car(self, response):
        self.curr_num_of_cars = self.curr_num_of_cars + 1
        if(self.curr_num_of_cars > self.MAX_NUM_OF_CARS):
            os._exit(0)

        def extract_with_css(query):
            return response.css(query).get(default = '').strip()

        yield {
            'stanje': extract_with_css('div.uk-width-1-2:contains("Stanje") + div.uk-text-bold::text'),
            'marka': extract_with_css('div.uk-width-1-2:contains("Marka") + div.uk-text-bold::text'),
            'model': extract_with_css('div.uk-width-1-2:contains("Model") + div.uk-text-bold::text'),
            'godiste': extract_with_css('div.uk-width-1-2:contains("Godište") + div.uk-text-bold::text'),
            'kilometraza': extract_with_css('div.uk-width-1-2:contains("Kilometraža") + div.uk-text-bold::text'),
            'karoserija': extract_with_css('div.uk-width-1-2:contains("Karoserija") + div.uk-text-bold::text'),
            'gorivo': extract_with_css('div.uk-width-1-2:contains("Gorivo") + div.uk-text-bold::text'),
            'kubikaza': extract_with_css('div.uk-width-1-2:contains("Kubikaža") + div.uk-text-bold::text'),
            'snaga_motora': extract_with_css('div.uk-width-1-2:contains("Snaga motora") + div.uk-text-bold::text'),
            'menjac': extract_with_css('div.uk-width-1-2:contains("Menjač") + div.uk-text-bold::text'),
            'broj_vrata': extract_with_css('div.uk-width-1-2:contains("Broj vrata") + div.uk-text-bold::text'),
            'boja': extract_with_css('div.uk-width-1-2:contains("Boja") + div.uk-text-bold::text'),
            'ostecenje': extract_with_css('div.uk-width-1-2:contains("Oštećenje") + div.uk-text-bold::text'),
            'klima': extract_with_css('div.uk-width-1-2:contains("Klima") + div.uk-text-bold::text'),
            'lokacija': extract_with_css('.infoBox.js-tutorial-contact .uk-grid.uk-margin-top-remove .uk-width-1-2::text'),
            'cena': extract_with_css('.financing span.priceClassified.regularPriceColor::text'),
            'url': response.request.url,
        }