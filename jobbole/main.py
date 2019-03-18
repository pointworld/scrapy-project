import os
import sys

from scrapy import cmdline


# 将当前文件所在的路径加入到 python 模块的解析路径集中
current_dir = os.path.abspath(__file__)
sys.path.append(current_dir)

cmdline.execute('scrapy crawl jobbole'.split())

