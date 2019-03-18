import os
import sys

from scrapy import cmdline

current_dir = os.path.abspath(__name__)
sys.path.append(current_dir)

# cmdline.execute('scrapy crawl github'.split())
# cmdline.execute('scrapy crawl github1'.split())
cmdline.execute('scrapy crawl github2'.split())

