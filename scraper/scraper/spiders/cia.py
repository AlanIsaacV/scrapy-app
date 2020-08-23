import scrapy


class SpiderCIA(scrapy.Spider):
    name = 'cia'
    start_urls = [
        'https://www.cia.gov/library/readingroom/historical-collections'
    ]
    custom_settings = {
        'FEED_URI': 'cia.json',
        'FEED_FORMAT': 'json',
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    def parse(self, response, **kwargs):
        links_css = 'a[href^=collection]::attr(href)'
        links_declassified = set(response.css(links_css).getall())
        for link in links_declassified:
            url = response.urljoin(link)
            yield response.follow(link, callback=self.parse_declassified, cb_kwargs={'url': url})

    def parse_declassified(self, response, **kwargs):
        title = response.css('.documentFirstHeading::text').get()
        body = response.css('.field-item.even p:not(class)::text').getall()

        yield {'url': kwargs['url'],
               'title': title,
               'body': body}
