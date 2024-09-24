import scrapy
import re

class PRIN1AnnexSpider(scrapy.Spider):
    name = "PRIN2"
    allowed_domains = ["www.fca.org.uk"]
    start_urls = ["https://www.handbook.fca.org.uk/handbook/PRIN/2/?view=chapter"]

    def parse(self, response):
        table_rows = response.css("table tr")
        
        for row in table_rows:
            section = "PRIN 2.1 The Principles"
            dated = "01/01/2021"
            
            description = []
            
    
            paragraphs = row.xpath('.//p')
            for p in paragraphs:
                text = ' '.join(p.xpath('.//text()').getall()).strip()
                if text:
                    description.append(text)
            
            
            list_items = row.xpath('.//li')
            for li in list_items:
                text = ' '.join(li.xpath('.//text()').getall()).strip()
                if text:
                    description.append(f"- {text}")

            
            content_text = ' '.join(description)
            content_text = re.sub(r'\s+', ' ', content_text).strip()

            if content_text:
                yield {
                    "Section": section,
                    "Dated": dated,
                    "Description": content_text,
                }

    def closed(self, reason):
        self.logger.info(f"Spider closed: {reason}")