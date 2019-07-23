# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


from jd_whole_spider.spiders.jd_category import JdCategorySpider
from jd_whole_spider.spiders.jd_product import JdProductSpider
from pymongo import MongoClient
from jd_whole_spider.settings import MONGODB_URL

class CategorySpiderPipeline(object):

	def open_spider(self,spider):
		'''
		开始时执行
		链接MongoDB数据库, 获取要操作的集合
		'''
		#判断spider是否是JDCategorySpider的实例对象 
		if isinstance(spider,JdCategorySpider):
			self.client = MongoClient(MONGODB_URL)

			self.category = self.client['jd']['category']

	def process_item(self, item, spider):
		if isinstance(spider,JdCategorySpider):
			self.category.insert_one(dict(item))
		return item
	def close_spider():
		if isinstance(spider,JdCategorySpider):
			self.client.close()

class ProductSpiderPipeline(object):

	def open_spider(self,spider):
		'''
		开始时执行
		链接MongoDB数据库, 获取要操作的集合
		'''
		#判断spider是否是JDCategorySpider的实例对象 
		if isinstance(spider,JdProductSpider):
			self.client = MongoClient(MONGODB_URL)

			self.category = self.client['jd']['product']

	def process_item(self, item, spider):
		if isinstance(spider,JdProductSpider):
			self.category.insert_one(dict(item))
		return item
	def close_spider():
		if isinstance(spider,JdProductSpider):
			self.client.close()

