# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
'''
定义数据模型：
	分类数据模型
	商品数据模型
'''

class JdWholeSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass



'''
类别数据模型字段，用于存储类别信息
	b_category_name: 大类别名称
	b_category_url: 大类别URL
	m_category_name: 中分类名称
	m_category_url: 中分类URL
	s_category_name: 小分类名称
	s_category_url: 小分类URL
'''
class Category(scrapy.Item):
	#大分类名称
	b_category_name = scrapy.Field()
	#大分类url
	b_category_url = scrapy.Field()
	#中分类名称
	m_category_name = scrapy.Field()
	#中分类url
	m_category_url = scrapy.Field()
	#小分类名称
	s_category_name = scrapy.Field()
	#小分类url
	s_category_url = scrapy.Field()


'''
商品数据模型类: 用于存储商品信息(Product)
字段:

product_category: 商品类别
product_sku_id: 商品ID
product_name: 商品名称
product_img_url: 商品图片URL
product_book_info: 图书信息, 作者,出版社
product_option: 商品选项
product_shop: 商品店铺
product_comments: 商品评论数量
product_ad: 商品促销
product_price: 商品价格
'''
class Product(scrapy.Item):
	#商品类别
	product_category = scrapy.Field()
	#商品类别ID
	product_category_id = scrapy.Field()
	#商品ID
	product_sku_id = scrapy.Field()
	#商品名称 
	product_name = scrapy.Field()
	#商品图片URL
	product_img_url = scrapy.Field()
	#图书信息, 作者,出版社 
	product_book_info = scrapy.Field()
	#商品选项
	product_option = scrapy.Field()
	#商品店铺
	product_shop = scrapy.Field()
	#商品评论数量
	product_comments = scrapy.Field()
	#商品促销
	product_ad = scrapy.Field()
	#商品价格
	product_price = scrapy.Field()


