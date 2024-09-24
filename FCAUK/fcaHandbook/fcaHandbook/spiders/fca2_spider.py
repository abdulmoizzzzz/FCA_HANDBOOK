import scrapy

class FcaSpiderSpider(scrapy.Spider):
    name = "fca2_spider"
    allowed_domains = ["handbook.fca.org.uk"]
    start_urls = ["https://www.handbook.fca.org.uk/handbook"]
    
    def parse(self, response):
        # Find the "High Level Standards" section
        high_level_standards = response.xpath('//li[contains(@class, "nonContentLink")]/a[contains(text(), "High Level Standards")]')
        
        if high_level_standards:
            # Extract the main category information
            main_category = "High Level Standards"
            main_link = high_level_standards.xpath('@href').get()
            
            yield {
                "main_category": main_category,
                "title": main_category,
                "link": response.urljoin(main_link),
                "type": "main"
            }
            
            # Finding the "PRIN Principles for Businesses" section
            prin_section = high_level_standards.xpath('../ul/li[contains(@class, "nonContentLink")]/a[contains(text(), "PRIN Principles for Businesses")]')
            
            if prin_section:
                title = prin_section.xpath('normalize-space(text())').get()
                link = prin_section.xpath('@href').get()
                
                yield {
                    "main_category": main_category,
                    "title": title,
                    "link": response.urljoin(link),
                    "type": "parent"
                }
                
                # Finding all sub-items for PRIN
                sub_items = prin_section.xpath('../ul//li/a')
                for sub_item in sub_items:
                    sub_title = sub_item.xpath('normalize-space(text())').get()
                    sub_link = sub_item.xpath('@href').get()
                    
                    yield {
                        "main_category": main_category,
                        "parent": title,
                        "title": sub_title,
                        "link": response.urljoin(sub_link),
                        "type": "sub"
                    }
            else:
                self.logger.warning("PRIN Principles for Businesses section not found")
        else:
            self.logger.warning("High Level Standards section not found")

    def closed(self, reason):
        self.logger.info(f"Spider closed: {reason}")