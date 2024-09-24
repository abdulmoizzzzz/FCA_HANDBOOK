import scrapy

class FcaSpiderSpider(scrapy.Spider):
    name = "fca_spider"
    allowed_domains = ["handbook.fca.org.uk"]
    start_urls = ["https://www.handbook.fca.org.uk/handbook"]
    

    def parse(self, response):
        
        top_level_items = response.xpath('//li[@class="nonContentLink"]/a[starts-with(@href, "/handbook/")]')
        
        for item in top_level_items:
            parent_title = item.xpath('normalize-space(text())').get()
            link = item.xpath('@href').get()
            
            
            yield {
                "parent_title": parent_title,
                "link": response.urljoin(link),
                
            }
            
            # Extracting the  sub-items
            sub_items = item.xpath('../ul//li/a[starts-with(@href, "/handbook/")]')
            for sub_item in sub_items:
                sub_title = sub_item.xpath('normalize-space(text())').get()
                sub_link = sub_item.xpath('@href').get()
                
                
                yield {
                    "parent": parent_title,
                    "title": sub_title,
                    "link": response.urljoin(sub_link),
                    
                }