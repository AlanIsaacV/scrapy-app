import scrapy

class Quotes(scrapy.Spider):
	name = 'quotes'
	start_urls = [ 
		'http://quotes.toscrape.com/'
	]

	def parse(self, response, **kwargs):
		title = response.css('h1 a::text').get()
		quotes = response.css('.text::text').getall()
		top_tags = response.css('.tag-item .tag::text').getall()

		print('*'*10)
		print('\n\n')

		print(f'Titulo:  {title}')
		print('\n')

		print(f'Citas: ')
		for quote in quotes:
			print(f'  - {quote}')
		print('\n\n')

		print(f'Top ten tags: ')
		for tag in top_tags:
			print(f'  - {tag}')

		print('\n\n')
		print('*'*10)