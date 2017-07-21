#!/usr/bin/python
# coding=utf-8
#encoding=utf-8
#-*-coding:UTF-8-*-

import re
import requests
import os
import tarfile
import time

# 爬取数据，并保存在position定义的路径
class Spider:
    def savePageInfo(self, _url, _position, _regX, _position_end):

        url = _url
        position = _position
        position_end = str(_position_end).decode('utf-8')
        html = requests.get(url).text

        regX = _regX

        pic_url = re.findall(regX,html,re.S)

        i = 0
        for each in pic_url:
            pic = requests.get( each )
            if not os.path.isdir(position):
                os.makedirs(position)

                fp = open(position + position_end + str(i).decode('utf-8') + '.jpg', 'wb')
            fp.write(pic.content)
            print (each[-15:])
            fp.close()
            i+=1


# 压缩文件，保存成tar.gz文件
def make_targz(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))


# 定义需要爬取的网站or页面，并定义正则表达式规则
def down_pic(start_from_num,stop_at_num):
    for position_end in range (start_from_num,stop_at_num):
        url = 'http://www.jdlingyu.moe/' + str(position_end).decode('utf-8')
        position = '/home/pyadm/jdly/jdly' + str(start_from_num).decode('utf-8') + '/'
        regX = r'original="(.+?\.jpg)"'
        spider = Spider()
        spider.savePageInfo(url, position, regX, position_end)


# 初始化数据
start_from_num = 10000
stop_at_num = 10999


# 递归执行爬虫，每次爬取1000个num，页面数未知，每间隔一分钟执行一次
for i in range(0,10):
    print ("Start: %s" % time.ctime())
    down_pic(start_from_num, stop_at_num)
    tar_name = str(start_from_num).decode('utf-8') + ".tar.gz"
    tar_path = "/home/pyadm/jdly/jdly" + str(start_from_num).decode('utf-8') + "/"
    start_from_num += 1000
    stop_at_num += 1000
    make_targz(tar_name, tar_path)
    time.sleep(60)
    print ("End: %s" % time.ctime())
