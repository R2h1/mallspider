import pickle
from pymongo import MongoClient
from redis import StrictRedis
from jd_whole_spider.settings import MONGO_URL,REDIS_URL
from jd_whole_spider.spiders.jd_product import JdProductSpider


def add_category_to_redis():
	#链接mongoDB
	mongo = MongoClient(MONGO_URL)
	#链接redis
	redis = StrictRedis.from_url(REDIS_URL)
	#获取操作集合
	collection = mongo['jd']['category']
	#游标读取分类信息
	cursor = collection.find()

	for category in cursor:
		#数据序列化
		data = pickle.dumps(category)
		#添加到redis_key指定的list
		redis.lpush(JdProductSpider.redis_key,data)

	#关闭MongoDB
	mongo.close()

if __name__ == '__main__':
	add_category_to_redis()

