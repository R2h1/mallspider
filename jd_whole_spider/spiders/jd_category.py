# -*- coding: utf-8 -*-
import scrapy
import json

from jd_whole_spider.items import Category


class JdCategorySpider(scrapy.Spider):
	name = 'jd_category'
	allowed_domains = ['3.cn']
	start_urls = ['https://dc.3.cn/category/get']
	

	def parse(self, response):
		#print(response.body.decode('GBK'))

		result = json.loads(response.body.decode('GBK'))
		datas = result['data']
		#小分类数量，即总分类数量
		#category_counts = 0
		#遍历数据列表获取大分类
		for data in datas:
			b_category = data['s'][0]
			#大分类信息
			b_category_info = b_category['n']
			#print('大分类：{}'.format(b_category_info))

			category_item = Category()
			category_item['b_category_name'],category_item['b_category_url'] = self.get_category_name_url(b_category_info)

			#中分类
			m_categorys = b_category['s']
			#遍历中分类列表
			for m_category in m_categorys:
				#中分类信息
				m_category_info = m_category['n']
				#print('中分类：{}'.format(m_category_info))
				category_item['m_category_name'],category_item['m_category_url'] = self.get_category_name_url(m_category_info)
				#小分类列表
				s_categorys = m_category['s']
				for s_category in s_categorys:
					#小分类信息
					s_category_info = s_category['n']
					#print('小分类：{}'.format(s_category_info))
					category_item['s_category_name'],category_item['s_category_url'] = self.get_category_name_url(s_category_info)
					#print(category_item)
					#category_counts += 1

					#将数据交给引擎
					yield category_item



	def get_category_name_url(self,category_info):
		'''
		根据分类信息，提取名称和url
		:param category_info:分类信息
		：return：分类的名称和url
		'''
		category = category_info.split('|')
		#分类url
		category_url = category[0]
		#分类名称
		category_name  = category[1]

		#第一类url都带有jd.com
		if category_url.count('jd.com') == 1:
			category_url = 'https://' + category_url
		elif category_url.count('_') == 1:
			category_url = 'https://channel.jd.com/{}.html'.format(category_url)
		else:
			category_url = category_url.replace('_',',')
			category_url = 'https://list.jd.com/list.html?cat={}'.format(category_url)

		#返回
		return category_name,category_url


