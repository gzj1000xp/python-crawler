#!/usr/bin/python

#-*-coding:utf-8-*-
import re
import requests
import os
import tarfile

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


def make_targz(output_filename, source_dir):
	with tarfile.open(output_filename, "w:gz") as tar:
		tar.add(source_dir, arcname=os.path.basename(source_dir))

start_from_num = 32000
stop_at_num = 32999
tar_name = str(start_from_num) + ".tar.gz"
tar_path = "/home/pyadm/222/jdly" + str(start_from_num) + "/"
#store_path="/home/pyadm/222/jdly/"

for position_end in range (start_from_num,stop_at_num):
	url = 'http://www.jdlingyu.moe/' + str(position_end)
	position = '/home/pyadm/222/jdly32000/' + str(position_end)
	regX = r'original="(.+?\.jpg)"'
	spider = Spider()
	spider.savePageInfo(url, position, regX)


make_targz(tar_name, tar_path)
