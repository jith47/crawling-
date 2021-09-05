import scrapy
from scrapy.crawler import CrawlerProcess


def parse_items(response):
    breadcrumbs = response.xpath('//a[@class="breadcrumbs-list__link"]/text()').getall()
    image_url = response.xpath('//a[@class="show-gallery"]/@href').get()
    brand = response.xpath("//h1[@class='title']/text()").get()
    pn = response.xpath("//span[@class='product-detail-label']/text()").get()
    pn1 = response.xpath("//a[@href='/collections/carbon38']/text()").get()
    product_name = pn+pn1
    pr = response.xpath('//span[contains(.,"$")]/text()').get()
    price = str(pr)
    reviews = response.xpath("//div[@class='okeReviews-reviewsSummary-ratingCount']/span/text()").get()
    if reviews is None:
        reviews = "0 Reviews"
    size = response.xpath('//*[@id="SingleOptionSelector-1"]/option/text()').getall()
    colour = response.xpath('//*[@id="SingleOptionSelector-0"]/option/text()').getall()
    t = response.xpath('/html/head/meta[4]/@content').get()
    description = str(t)
    sku = response.xpath('//p[contains(.,"SKU")]/text()').get()
    yield {
        'breadcrumbs': breadcrumbs,
        'image_url': response.css('a.show-gallery').xpath('@href').get(),
        'brand': response.css("h1.title::text").get(),
        'product_name': pd_name,
        'price': price.strip(),
        'reviews': reviews,
        'colour': colour,
        'sizes': size,
        'description': desc.strip(),
        'sku': sku
    }

class ScrapSpider(scrapy.Spider):
    name = 'posts'
    start_urls = ['https://carbon38.com/collections/tops']

    def parse(self, response):
        lst = []
        for quotes in response.css("a.product-link").xpath("@href"):
            lst.append(quotes)
        q = len(lst)
        for i in range(0, q):
            url = lst[i]
            yield response.follow(url.extract(), callback=self.parse_items)
        next_page = response.css('li.item.pages-item-next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    
#run spider
process = CrawlerProcess()
process.crawl(ScrapSpider)
process.start()
