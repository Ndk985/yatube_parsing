import scrapy


class GroupSpider(scrapy.Spider):
    name = "group"
    allowed_domains = ["158.160.177.221"]
    start_urls = ["http://158.160.177.221"]

    def parse(self, response):
        # Ищем все ссылки на группы по классу group_link
        all_groups = response.css('a.group_link[href^="/group/"]')
        for group in all_groups:
            yield response.follow(group, callback=self.parse_group)

        # Обработка пагинации
        next_page = response.xpath("//a[contains(., 'Следующая')]/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_group(self, response):
        # Извлекаем количество записей (правильный селектор)
        posts_text = response.css('div.h6.text-muted::text').get()
        posts_count = int(posts_text.split(':')[1].strip()) if posts_text else 0

        yield {
            'group_name': response.css('div.card-body h2::text').get().strip(),
            'description': response.css('p.group_descr::text').get(default='').strip(),  # Обратите внимание на group_descr вместо group-descr
            'posts_count': posts_count
        }
