# -*- coding: utf-8 -*-
import scrapy
import json
import pickle
from jsonpath import jsonpath
from jd_whole_spider.items import Product
from scrapy_redis import RedisSpider

'''
商品信息爬虫
	重写start_requests方法, 根据分类信息构建列表页的请求
	解析列表页,提取商品的skuid, 构建商品基本的信息请求; 实现翻页
	解析商品基本信息, 构建商品促销信息的请求
	解析促销信息,构建商品评价信息的请求,
	解析商品评价信息, 构建价格信息的请求
	解析价格信息
'''

class JdProductSpider(RedisSpider):
	name = 'jd_product'
	allowed_domains = ['jd.com','p.3.cn']
	#用于指定分布式爬虫的起始url列表，在redis数据库中的key
	redis_key = 'jd_product:category'
	#start_urls = ['http://jd.com/']

	#def start_requests(self):
		#category = {
			#'b_category_name':'家用电器',
			#'b_category_url':'https://jiadian.jd.com',
			#'m_category_name':'洗衣机',
			#'m_category_url':'https://list.jd.com/list.html?cat=737,794,880',
			#'s_category_name':'洗衣机配件',
			#'s_category_url':'https://list.jd.com/list.html?cat=737,794,877'
		#}

		#scrapy.Request(url,callback,meta),请求url,callback回调函数，meta为传递的数据
		#yield scrapy.Request(category['s_category_url'],callback=self.parse,meta={'category':category})

	#重写make_request_from_data()方法，
	def make_request_from_data(self,data):
		'''
		根据redis中读取的二进制数据，构建请求
		:params data:分类信息的二进制数据
		:return:小分类url,构建的请求对象
		'''
		#分类信息的二进制数据转换为字典
		category = pickle.loads(data)
		#使用return返回请求
		return scrapy.Request(category['s_category_url'],callback=self.parse,meta={'category':category})


	def parse(self, response):
		category = response.meta['category']
		#解析列表页，提取商品的skuid，extract（）返回一个list
		sku_ids = response.xpath('//div[contains(@class, "j-sku-item")]/@data-sku').extract()
		for sku_id in sku_ids:
			#创建商品对象
			product_item = Product()
			#商品类别，这里使用meta传递过来的catagory
			product_item['product_category'] = category
			#商品ID
			product_item['product_sku_id'] = sku_id
			#构建商品基本信息的请求url
			product_baseinfo_url = 'https://cdnware.m.jd.com/c1/skuDetail/apple/7.3.4/{}.json'.format(sku_id)
			yield scrapy.Request(product_baseinfo_url,callback=self.parse_product_info,meta={'product_item':product_item})
		#从第一页获获取所有的下一页
		next_url = response.xpath('//a[@class="pn-next"]/@href').extract_first()

		if next_url:
			#url补全，将基地址和相对地址链接成绝对地址，相当于替换基地址中的相对地址部分
			next_url = response.urljoin(next_url)

			#请求下一页然后循环解析列表页
			yield scrapy.Request(next_url,self.parse,meta={'category':category})


	def parse_product_info(self,response):
		#取出传递过来的meta数据
		product_item = response.meta['product_item']

		#开始解析:商品名称,商品图片URL， 商品选项,	商品店铺,商品类别ID，图书信息作者出版社 

		#json转换为字典
		result = json.loads(response.text)

		product_item['product_name'] = result['wareInfo']['basicInfo']['name']

		product_item['product_img_url'] = result['wareInfo']['basicInfo']['wareImage'][0]['small']

		book_info = jsonpath(result,'$..booinfo')
		if book_info:
			product_item['product_book_info'] = {
				"author": book_info[0]['author'],
				"publisher":book_info[0]['publisher']: 
			}

		#jsonpath返回列表，而colorSize键的值也为列表
		color_size = jsonpath(result,'$..colorSize')
		if color_size:
			option_title = color_size[0][0]['title']
			product_option=[]
			title = option['title']
			for option in color_size[0][0]['buttons']:
				prduct_option.append(option['text'])
			product_item["product_option"]={
				title:product_option
			}


		shop = jsonpath(result,'$..shop')
		if shop:
			shop = shop[0]
			if shop:
				#商品店铺信息
				product_item['product_shop']={
					'shop_id':shop['shopId'],
					'shop_name':shop['name'],
					'shop_score':shop['score']
				}
			else:
				product_item['product_shop']={
					'shop_name':'jd自营'
				}
		#商品分类ID
		product_item['product_category_id'] = result['wareInfo']['basicInfo']['category'].replace(';',',')
		#print(product_item)

		#促销信息的url
		ad_url = 'https://cd.jd.com/promotion/v2?skuId={}&area=22_1930_4284_0&cat={}'\
			.format(product_item['product_sku_id'],product_item['product_category_id'])
		yield scrapy.Request(ad_url,callback=self.parse_product_ad,meta={'product_item':product_item})

	def parse_product_ad(self,response):
		product_item = response.meta['product_item']
		result = json.loads(response.body.decode('GBK'))
		#商品促销
		product_item['product_ad'] = jsonpath(result,'$..ad')[0] if jsonpath(result,'$..ad') else ''

		#评价信息url
		comments_url = 'https://club.jd.com/comment/productCommentSummaries.action?referenceIds={}'\
			.format(product_item['product_sku_id'])
		yield scrapy.Request(comments_url,self.parse_comment,meta={'product_item':product_item})

	def parse_comment(self,response):
		product_item = response.meta['product_item']
		result = json.loads(response.text)
		#商品评论数量
		product_item['product_comments'] = {
            "评论数":jsonpath(result,'$..CommentCount')[0], 
            "好评数":jsonpath(result,'$..GoodCount')[0], 
            "好评率":jsonpath(result,'$..GoodRate')[0],  
            "差评数":jsonpath(result,'$..PoorCount')[0], 
		}
		#价格信息url
		price_url = 'https://p.3.cn/prices/mgets?skuIds=J_{}'.format(product_item['product_sku_id'])

		yield scrapy.Request(price_url,self.parse_price,meta={'product_item':product_item})


	def parse_price(self,response):
		product_item = response.meta['product_item']
		result =  json.loads(response.text)
		#商品价格
		product_item['product_price'] = result[0]['p']
		yield product_item


		

		




		



	
		
	
		


