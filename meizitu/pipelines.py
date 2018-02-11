# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import urllib
import requests

from meizitu import settings

import time

class MeizituPipeline(object):

    def process_item(self, item, spider):
        header = {
            'USER-Agent': 'User-Agent:Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            'Cookie': 'b963ef2d97e050aaf90fd5fab8e78633'
            # 需要查看图片的cookie信息，否则下载的图片无法查看
        }
        dir_path = '%s\%s' % (settings.IMAGES_STORE, spider.name)  # 存储路径
        title = item['name']
        print ('dir_path', dir_path+"\\image\\"+title)
        path = dir_path+"\\image\\"+title
        print path
        if not os.path.exists(path):
            os.makedirs(path)
        for image_url in item['image_urls']:
            list_name = image_url.split('/')
            file_name = list_name[len(list_name) - 1]  # 图片名称
            # print 'filename',file_name
            file_path = '%s/%s' % (path, file_name)
            # print 'file_path',file_path
            if os.path.exists(file_name):
                continue
            with open(file_path, 'wb') as file_writer:
                # conn = urllib.urlopen(image_url,hearder=header)  # 下载图片
                time.sleep(1)
                conn = requests.get(image_url,headers=header)
                file_writer.write(conn.content)
            file_writer.close()
        return item
