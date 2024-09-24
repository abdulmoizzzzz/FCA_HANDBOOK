import scrapy
import re

class PRINTP1Spider(scrapy.Spider):
    name = "PRINTP1"
    allowed_domains = ["www.fca.org.uk"]
    start_urls = ["https://www.handbook.fca.org.uk/handbook/PRIN/TP/1/1.html"]

    def parse(self, response):
        
        table_rows = response.xpath("//table//tr")[1:]

        current_item = {}
        for row in table_rows:
            cells = row.xpath('./td')
            if len(cells) >= 4: 
                if current_item:
                    yield current_item
                current_item = self.extract_row_data(row)
            elif len(cells) > 0:  
                self.update_item_with_continuation(current_item, row)

        if current_item:  
            yield current_item

    def extract_row_data(self, row):
        section = "PRIN TP 1 Transitional provisions"

        material = row.xpath('.//td[2]//text() | .//td[2]//*/text()').getall()
        provision = row.xpath('.//td[4]//text() | .//td[4]//*/text()').getall()
        dates_in_force = row.xpath('.//td[5]//text() | .//td[5]//*/text()').getall()
        coming_into_force = row.xpath('.//td[6]//text() | .//td[6]//*/text()').getall()

        return {
            "Section": section,
            "Material to which the transitional provision applies": self.clean_text(material),
            "Transitional Provision": self.clean_text(provision),
            "Transitional Provision: dates in force": self.clean_text(dates_in_force),
            "Handbook provision: coming into force": self.clean_text(coming_into_force),
        }

    def update_item_with_continuation(self, item, row):
        continuation_text = row.xpath('.//td//text() | .//td//*/text()').getall()
        cleaned_text = self.clean_text(continuation_text)
        
    
        item["Transitional Provision"] += " " + cleaned_text

    def clean_text(self, text_list):
        text = ' '.join(text_list)
        text = re.sub(r'\s+', ' ', text).strip()
        text = re.sub(r'<[^>]+>', '', text) ##removing html tags from text
        return text if text else ''

    def closed(self, reason):
        self.logger.info(f"Spider closed: {reason}")