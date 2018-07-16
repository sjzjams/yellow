# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from yellow.settings import FILES_STORE
from yellow.settings import DEFAULT_REQUEST_HEADERS
import requests
import sys
import importlib
importlib.reload(sys)
from contextlib import closing


class YellowPipeline(object):
    def process_item(self, item, spider):

        with open(FILES_STORE + "/db.txt", "a+") as fp:
            s = item['url'] + "#!#" + item['img']
            fp.write(s)
            fp.write("\n")

        fp.close()
        url = item['url']
        img =  item['img']
        imgName = img.split("/")[-1]


        """
        下载图片
        """
        #with open(FILES_STORE + "/" + "{}".format(imgName),'wb') as f:
        #   req = requests.get(img, headers = DEFAULT_REQUEST_HEADERS)
        #    f.write(req.content)

        #f.close()
        print(url+"分割线")
        with closing(requests.get(url, stream=True)) as response:
            chunk_size = 1024
            content_size = int(response.headers['content-length'])
            videoName = url.split("/")[-1]
            progress = ProgressBar(videoName, total=content_size, unit="KB", chunk_size=chunk_size, run_status="正在下载", fin_status="下载完成")

            with open(FILES_STORE + "/" + videoName, "wb") as file:
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    progress.refresh(count=len(data))


        return item

'''
下载进度
'''
class ProgressBar(object):
    def __init__(self, title, count=0.0, run_status=None, fin_status=None, total=100.0, unit='', sep='/',
                 chunk_size=1.0):
        super(ProgressBar, self).__init__()
        self.info = "[%s] %s %.2f %s %s %.2f %s"
        self.title = title
        self.total = total
        self.count = count
        self.chunk_size = chunk_size
        self.status = run_status or ""
        self.fin_status = fin_status or " " * len(self.statue)
        self.unit = unit
        self.seq = sep

    def __get_info(self):
        # 【名称】状态 进度 单位 分割线 总数 单位
        _info = self.info % (
            self.title, self.status, self.count / self.chunk_size, self.unit, self.seq, self.total / self.chunk_size,
            self.unit)
        return _info

    def refresh(self, count=1, status=None):
        self.count += count
        # if status is not None:
        self.status = status or self.status
        end_str = "\r"
        if self.count >= self.total:
            end_str = '\n'
            self.status = status or self.fin_status
        print(self.__get_info(), end=end_str)