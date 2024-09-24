import scrapy

class PRIN1AnnexSpider(scrapy.Spider):
    name = "PRIN1Annex"
    allowed_domains = ["www.fca.org.uk"]
    start_urls = ["https://www.handbook.fca.org.uk/handbook/PRIN/1/Annex1.html"]

    def parse(self, response):
        table_rows = response.css("table tr")
        
        for row in table_rows:
            section = "PRIN 1 Annex 1 Non-designated investment business - clients that a firm may treat as an eligible counterparty for the purposes of PRIN"
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

            
            content_text = ' '.join(description).replace('\n\n', ' ').strip()

            if content_text:
                yield {
                    "Section": section,
                    "Dated": dated,
                    "Description": content_text,
                }

    def closed(self, reason):
        self.logger.info(f"Spider closed: {reason}")