# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import JsonLinesItemExporter

class TiebaPipeline:
    def __init__(self):
        self.fp = open('bky.json','wb')
        self.exporter = JsonLinesItemExporter(self.fp,ensure_ascii=False,encoding='utf-8')
        self.exporter.start_exporting()

    def open_spider(self,spider):
        print('爬虫开始......')
    def process_item(self, item, spider):
        self.exporter.export_item(item)

    def close_spider(self,spider):
        self.fp.close()
        print('爬虫完成了')
