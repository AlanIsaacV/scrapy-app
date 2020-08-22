import scrapy


class Quotes(scrapy.Spider):
    name = 'quotes'

    custom_settings = {
        'FEED_URI': 'quotes.json',
        'FEED_FORMAT': 'json'
    }

    start_urls = [
        'http://quotes.toscrape.com/'
    ]

    def parse(self, response, **kwargs):
        title = response.css('h1 a::text').get()
        top_tags = response.css('.tag-item .tag::text').getall()

        top = getattr(self, 'top', None)
        top_tags = top_tags[:int(top)] if top else top_tags

        data = {'title': title,
                'top tags': top_tags,
                'quotes': self.get_quotes(response)
                }
        yield self.next_page(response, data)

    def parse_quotes(self, response, **kwargs):
        kwargs['quotes'].extend(self.get_quotes(response))
        yield self.next_page(response, kwargs)

    def get_quotes(self, response):
        quotes = response.css('.quote')
        quotes_list = []
        for quote in quotes:
            quotes_list.append({
                'text': quote.css('.text::text').get(),
                'author': quote.css('.author::text').get(),
                'tags': quote.css('.tags .tag::text').getall(),
            })
        return quotes_list

    def next_page(self, response, data):
        next_page_link = response.css('.next a::attr(href)').get()
        if next_page_link:
            return response.follow(next_page_link, callback=self.parse_quotes, cb_kwargs=data)
        else:
            return data
