# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo


class MongoDBPipeline:

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.collection_empty = False  # Flag to track if collection is emptied

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DB"),
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def empty_collection(self, collection_name):
        self.db[collection_name].delete_many({})
        self.collection_empty = True

    def process_item(self, item, spider):
        
        if spider.name == 'PRIN1.1':  
            raw_collection = "PRIN1.1ApplicationandPurpose"
            
        elif spider.name == 'PRIN1.2':  
            raw_collection = "PRIN1.2ClientsAndPrinciples"
        
        elif spider.name == 'PRIN1Annex':  
            raw_collection = "PRIN1ANNEX1"

        elif spider.name == 'PRIN2':  
            raw_collection = "PRIN2.1ThePrinciples"

        elif spider.name == 'PRIN2A.1':  
            raw_collection = "PRIN2A.1ApplicationandPurpose"

        elif spider.name == 'PRIN2A.2':  
            raw_collection = "PRIN2A.2CrossCuttingObligations"

        elif spider.name == 'PRIN2A.3':  
            raw_collection = "PRIN2A.3productsandservices"

        elif spider.name == 'PRIN2A.4':  
            raw_collection = "PRIN2A.4priceandvalue"

        elif spider.name == 'PRIN2A.5':  
            raw_collection = "PRIN2A.5outcomeonconsumerunderstanding"

        elif spider.name == 'PRIN2A.6':  
            raw_collection = "PRIN2A.6outcomeonconsumersupport"

        elif spider.name == 'PRIN2A.7':  
            raw_collection = "PRIN2A.7General"

        elif spider.name == 'PRIN2A.8':  
            raw_collection = "PRIN2A.8Governanceandculture"

        elif spider.name == 'PRIN2A.9':  
            raw_collection = "PRIN2A.9Monitoringofconsumeroutcomes"

        elif spider.name == 'PRIN2A.10':  
            raw_collection = "PRIN2A.10Redressorotherappropriateaction"

        elif spider.name == 'PRIN2A.11':  
            raw_collection = "PRIN2A.11Saleandpurchaseofproductbooks"

        elif spider.name == 'PRIN3.1':  
            raw_collection = "PRIN3.1WHO"

        elif spider.name == 'PRIN3.2':  
            raw_collection = "PRIN3.2WHAT"

        elif spider.name == 'PRIN3.3':  
            raw_collection = "PRIN3.3WHERE"

        elif spider.name == 'PRIN3.4':  
            raw_collection = "PRIN3.4GENERAL"

        elif spider.name == 'PRIN4.1':  
            raw_collection = "PRIN4.1PrinciplesMiFIDbusiness"

        elif spider.name == 'PRINTP1':  
            raw_collection = "PRINTPTransitionalprovisions"

        elif spider.name == 'PRINSch2':  
            raw_collection = "PRINSch2Notificationrequirements"

        elif spider.name == 'PRINSch5':  
            raw_collection = "PRINSch5Rightsofactionfordamages"
        
        elif spider.name == 'PRINSch6':  
            raw_collection = "PRINSch6Rulesthatcanbewaived"

        else:
            raise ValueError(f"Unknown spider: {spider.name}")

      
        if not self.collection_empty:
            self.empty_collection(raw_collection)
        self.db[raw_collection].insert_one(ItemAdapter(item).asdict())
        

        return item
