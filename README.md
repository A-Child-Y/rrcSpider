# rrcSpider

## 环境
1.  scrapy 框架
2.  mysql，zmail,第三方库

## 运行配置
1. 在settings.py 中 DB字段配置数据库名，本地要手动创建该数据库（mysql），该数据库中要有'dazhong', 'fute', 'bieke', 'xiandai'表名，每个表名中要有以下字段 title, update_purchase_time, update_mileage, money, down_payment。（如不想配置数据库，在rrc.py 和rrci.py中 注释 'ITEM_PIPELINES': {'RRC.pipelines.ImgPipeline': 300},  即可。）

2. 代理IP 可自己重新配置，目前该项目中已取消代理IP
3. 配置邮箱，可选，默认是配置邮箱，需要在settings.py,配置邮箱账号，如不配置可去注释掉，在rrc.py和rrci.py中，注释地方已标注。
