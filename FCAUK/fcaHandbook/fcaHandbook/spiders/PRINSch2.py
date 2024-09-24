import scrapy
import re

class PRIN2A1Spider(scrapy.Spider):
    name = "PRINSch2"
    allowed_domains = ["www.fca.org.uk"]
    start_urls = ["https://www.handbook.fca.org.uk/handbook/PRIN/Sch/2/2.html"]

    def parse(self, response):
        
        section = "PRIN Sch 2 Notification requirements"

        elements = response.xpath('//h2[@class="crosstitle"] | //div[contains(@class, "level")]')

        for element in elements:
            if element.xpath('name()').get() == 'h2':
                current_section = element.xpath('text()').get().strip()
            else:
                ID = element.xpath('.//span[@class="extended"]/text()').get()
                Dated = element.xpath('.//time/span/text()').get()

                
                Description = []
                table_data = {}

                # Extract paragraphs (non-table descriptions)
                paragraphs = element.xpath('.//p')
                for p in paragraphs:
                    text = ' '.join(p.xpath('.//text()').getall()).strip()
                    if text:
                        Description.append(text)

                # Extract list items (if any)
                list_items = element.xpath('.//li')
                for li in list_items:
                    text = ' '.join(li.xpath('.//text()').getall()).strip()
                    if text:
                        Description.append(f"- {text}")

                # Extract table data
                table_rows = element.xpath('.//tr')
                if table_rows:
                    headers = table_rows[0].xpath('.//p/strong/text()').getall()
                    data = table_rows[1].xpath('.//td/p').getall()

                    if headers and data:
                        for header, content in zip(headers, data):
                            cleaned_content = re.sub(r'<[^>]+>', '', content).strip()  # Remove HTML tags from content
                            table_data[header] = cleaned_content

                    # If table data exists, yield only the table data without adding it to the description
                    if table_data:
                        yield {
                            "Section": section,
                            "ID": ID,
                            "Dated": Dated,
                            "TableData": table_data,
                        }

                
                if Description and not table_data:
                    content_text = ' '.join(Description)
                    content_text = re.sub(r'\s+', ' ', content_text).strip()

                    if content_text:
                        yield {
                            "Section": section,
                            "ID": ID,
                            "Dated": Dated,
                            "Description": content_text,
                        }

    def closed(self, reason):
        self.logger.info(f"Spider closed: {reason}")
