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

        quotes = response.css('.quote')
        quotes_list = []
        for quote in quotes:
            quotes_list.append({
                'text': quote.css('.text::text').get(),
                'author': quote.css('.author::text').get(),
                'tags': quote.css('.tags .tag::text').getall(),
            })

        yield {'title': title,
               'top tags': top_tags,
               }

        next_page = response.css('.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse_quotes, cb_kwargs={'quotes': quotes_list})

    def parse_quotes(self, response, **kwargs):
        quotes = response.css('.quote')
        quotes_list = []
        for quote in quotes:
            quotes_list.append({
                'text': quote.css('.text::text').get(),
                'author': quote.css('.author::text').get(),
                'tags': quote.css('.tags .tag::text').getall(),
            })

        kwargs['quotes'].extend(quotes_list)

        next_page = response.css('.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse_quotes, cb_kwargs=kwargs)
        else:
            yield kwargs
