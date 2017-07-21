# -*- coding: utf-8 -*
import urllib
from sys import argv
import re
from bs4 import BeautifulSoup
import os
import requests


def getpage(nameid, pageid=1, wrongtry=0, leastlink=""):
    pageurl = u"http://bcy.net/u/%s/post/cos?p=%d" % (nameid, pageid)  # 获取页面地址
    print(pageurl)
    session = requests.session()
    html = session.get(pageurl, headers=headers)
    # 返回网页内容
    soup = BeautifulSoup(html.content, "html.parser")
    # print soup
    # 解析网页
    for asrc in soup.find_all('div', class_='postWorkCard__img ovf'):
        a_src = asrc.find('a').get('href')
        pageurl = "http://bcy.net/" + a_src
        print (pageurl)
        downpic(pageurl, nameid)
    if not pageurl == leastlink:
        pageid += 1
        leastlink = pageurl
        getpage(nameid, pageid, wrongtry, leastlink)
    else:
        pageid = pageid - 1
        print("共爬到%d页" % pageid)
        # 寻找内页地址


def downpic(pagelink, nameid):
    global picnum
    session1 = requests.session()
    html1 = session1.get(pagelink, headers=headers)
    soup1 = BeautifulSoup(html1.content, "html.parser")
    # print soup1

    for links in soup1.findAll('img', class_="detail_std"):
        img_src = links.get('src')
        img_src = re.sub(r'/w.*$', "", img_src)
        # print img_src
        picname = re.search(r"(?<=/post/).+?(?=$)", img_src, re.M)
        picname = re.search(r"(?<=/).+?(?=$)", picname.group(0), re.M)
        CurrentPath = os.getcwd()
        # filename = CurrentPath + "/bcy/%s_image/%s" % (nameid, picname.group(0))
        # filename = "/bcy/%s_image/%s" % (nameid, picname.group(0))
        filename = CurrentPath + u"\\bcy\%s_image\%s" % (nameid, picname.group(0))
        picnum = picnum + 1
        print( "-----------------")
        print( picname.group(0) )
        print( img_src )
        print( filename )
        print( u'下完了%s张' % picnum )
        print( "-----------------")
        try:
            urllib.request.urlretrieve(img_src, filename)
        except Exception:
            print(u'这张图片下载出问题了： %s' % filename)


# 程序入口
if __name__ == '__main__':
    page = 0
    member_id = "1208130"
    if not os.path.exists("bcy/%s_image" % member_id):
        os.makedirs("bcy/%s_image" % member_id)
        print("创建目录")
        # 创建目录
print ("存储在 PY文件目录/bcy 中")
user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
headers = {'User-Agent': user_agent, 'Referer': 'http://bcy.net'}
# 准备headers
pagenum = 0
picnum = 0
# 准备计次变量
getpage(member_id, 1)
