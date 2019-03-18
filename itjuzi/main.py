import os
import sys

from scrapy import cmdline

# 将当前文件所在的路径添加到 Python 的搜索模块的路径集
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

cmdline.execute('scrapy runspider ./itjuzi/spiders/juzi.py'.split())
