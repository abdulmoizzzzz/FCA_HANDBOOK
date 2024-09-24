import scrapy
import re

class PRIN2A11Spider(scrapy.Spider):
    name = "PRIN3.1"
    allowed_domains = ["www.fca.org.uk"]
    start_urls = ["https://www.handbook.fca.org.uk/handbook/PRIN/3/1.html"]

    def parse(self, response):
        
        current_section = "PRIN 3.1 Who?"

        elements = response.xpath('//div[contains(@class, "level")]')

        for element in elements:
            ID = element.xpath('.//span[@class="extended"]/text()').get()
            Dated = element.xpath('.//time/span/text()').get()

            Description = []

            
            paragraphs = element.xpath('.//p[not(.//li)]')
            for p in paragraphs:
                text = ' '.join(p.xpath('.//text()').getall()).strip()
                if text:
                    Description.append(text)

          
            list_paragraphs = element.xpath('.//p[.//li]')
            for p in list_paragraphs:
                text = ' '.join(p.xpath('text()').getall()).strip()
                if text:
                    Description.append(text)
                
                list_items = p.xpath('.//li')
                for li in list_items:
                    text = ' '.join(li.xpath('.//text()').getall()).strip()
                    if text:
                        Description.append(f"- {text}")

            content_text = ' '.join(Description)
            content_text = re.sub(r'\s+', ' ', content_text).strip()
            content_text = re.sub(r'^1\s*', '', content_text)

            if content_text:
                yield {
                    "Section": current_section,
                    "ID": ID,
                    "Dated": Dated,
                    "Description": content_text,
                }

    def closed(self, reason):
        self.logger.info(f"Spider closed: {reason}")