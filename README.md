# mallspider
使用scrapy,redis,mongodb实现的一个分布式爬虫，底层存储选择mongodb，分布式使用redis来实现。

针对https://www.jd.com/2019 网站，将其首页的分类信息——各级分类的名称和URL，商品详情信息——商品名称，商品价格，商品评论数量，商品店铺，商品促销，商品选项，商品图片的URL

避免爬虫被禁的策略：
  实现随机User-Agent下载中间件
  实现代理IP的中间件
 
  
