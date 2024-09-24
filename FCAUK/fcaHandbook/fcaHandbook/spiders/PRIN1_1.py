import scrapy

class IntroductionSpiderSpider(scrapy.Spider):
    name = "PRIN1.1"
    allowed_domains = ["www.fca.org.uk"]
    start_urls = ["https://www.handbook.fca.org.uk/handbook/PRIN/1/1.html"]

    def parse(self, response):
        guidance_elements = response.xpath('//div[contains(@class, "guidance")]')

        unique_items = {}
        
        for guidance in guidance_elements:
            
            Section = guidance.xpath('preceding::h2[@class="crosstitle"][1]/text()').get()
            
            ID = guidance.xpath('.//span[@class="extended"]/text()').get()
            Dated = guidance.xpath('.//time/span/text()').get()
            
            Description = []
            
            paragraphs = guidance.xpath('.//p')
            for p in paragraphs:
                text = ' '.join(p.xpath('.//text()').getall()).strip()
                if text:
                    Description.append(text)
            
            list_items = guidance.xpath('.//li')
            if list_items:
                for li in list_items:
                    text = ' '.join(li.xpath('.//text()').getall()).strip()
                    if text:
                        Description.append(f"- {text}")

            content_text = '\n\n'.join(Description)

            if content_text:
                content_key = content_text.strip()
                
                if content_key not in unique_items or (unique_items[content_key]['ID'] is None and unique_items[content_key]['Dated'] is None and (ID is not None or Dated is not None)):
                    unique_items[content_key] = {
                        "Section": Section,
                        "ID": ID,
                        "Dated": Dated,
                        "Description": content_text,  
                    }

        for item in unique_items.values():
            yield item

    def closed(self, reason):
        self.logger.info(f"Spider closed: {reason}")