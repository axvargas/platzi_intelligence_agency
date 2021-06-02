from scrapy import Spider

# Autoomatization
# curl -u a8bf052c1f72426ba0e7ecbea34f39bd: https://app.scrapinghub.com/api/run.json -d project=530175 -d spider=cia_spider
# curl -u APIKEY: https://storage.scrapinghub.com/items/PROJECT_ID/NUMBER_OF_SPIDER/NUMER_OF_JOB

# XPATH
LINKS_XPATH = '//a[starts-with(@href,"collection") and (parent::h3| parent::h2)]/@href'
TITLE_XPATH = '//h1[@class="documentFirstHeading"]/text()'
DESCRIPTION_XPATH = '//div[@class="field-item even"]/p[not(strong) and not(@style)]/descendant-or-self::*/text()'


class SpiderCIA(Spider):
    name = 'cia_spider'
    start_urls = ['https://www.cia.gov/readingroom/historical-collections']
    custom_settings = {
        'FEEDS': {
            'cia.json': {
                'format': 'json',
                'encoding': 'utf8',
                'fields': ['url', 'title', 'description'],
                'overwrite': True
            }
        },
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'
    }

    def parse_link(self, response, **kwargs):
        link = kwargs['url']
        title = response.xpath(TITLE_XPATH).get()
        description = response.xpath(DESCRIPTION_XPATH).getall()
        yield {
            'url': link,
            'title': title,
            'description': "".join(description)
        }

    def parse(self, response):
        declasified_links = response.xpath(LINKS_XPATH).getall()
        for link in declasified_links:
            yield response.follow(
                link,
                callback=self.parse_link,
                cb_kwargs={'url': response.urljoin(link)}
            )
