#!/usr/bin/python

#-*-coding:utf-8-*-
import re
import requests
import os
import tarfile
import time

#��ȡ���ݣ���������position�����·��
class Spider:
    def savePageInfo(self, _url, _position, _regX):

        url = _url
        position = _position
        html = requests.get(url).text

        regX = _regX

        pic_url = re.findall(regX,html,re.S)

        i = 0
        for each in pic_url:
            pic = requests.get( each )
            if not os.path.isdir(position):
                os.makedirs(position)

            fp = open( position+'/'+str(i)+'.jpg', 'wb' )
            fp.write(pic.content)
            print position+each
            fp.close()
            i+=1


#ѹ���ļ��������tar.gz�ļ�
def make_targz(output_filename, source_dir):
	with tarfile.open(output_filename, "w:gz") as tar:
		tar.add(source_dir, arcname=os.path.basename(source_dir))


#������Ҫ��ȡ����վorҳ�棬������������ʽ����
def down_pic(start_from_num,stop_at_num):
	for position_end in range (start_from_num,stop_at_num):
		url = 'http://www.jdlingyu.moe/' + str(position_end)
		position = '/home/pyadm/jdly/jdly' + str(start_from_num) + '/' + str(position_end)
		regX = r'original="(.+?\.jpg)"'
		spider = Spider()
		spider.savePageInfo(url, position, regX)


#��ʼ������
start_from_num = 10000
stop_at_num = 10999


#�ݹ�ִ�����棬ÿ����ȡ1000��num��ҳ����δ֪��ÿ���һ����ִ��һ��
for i in range(0,10):
	print "Start: %s" % time.ctime()
	down_pic(start_from_num, stop_at_num)
	tar_name = str(start_from_num) + ".tar.gz"
	tar_path = "/home/pyadm/jdly/jdly" + str(start_from_num) + "/"
	start_from_num += 1000
	stop_at_num += 1000
	make_targz(tar_name, tar_path)
	time.sleep(60)
	print "End: %s" % time.ctime()
