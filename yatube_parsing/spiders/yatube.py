import scrapy

from yatube_parsing.items import YatubeParsingItem


class YatubeSpider(scrapy.Spider):
    name = "yatube"
    allowed_domains = ["158.160.177.221"]
    start_urls = ["http://158.160.177.221/"]

    def parse(self, response):
        for post in response.css('div.card.mb-3.mt-1.shadow-sm'):
            data = {
                'author': post.css('strong.d-block.text-gray-dark::text').get().strip().replace('@', ''),
                'text': ' '.join(
                    t.strip() for t in post.css('p.card-text::text').getall()
                ).strip(),
                'date': post.css('small.text-muted::text').get().strip(),
            }
            yield YatubeParsingItem(data)

        next_page = response.xpath("//a[contains(., 'Следующая')]/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
