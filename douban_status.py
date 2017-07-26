# -*- coding: utf-8 -*
import urllib
from bs4 import BeautifulSoup
import os
import requests

# 从问题的页面中抽取出answerid
def getansid(questionid):
    pageurl = u"https://www.zhihu.com/question/%s" % (questionid)  # 获取页面地址
    session = requests.session()
    html = session.get(pageurl, headers=headers)
    # 返回网页内容
    soup = BeautifulSoup(html.content, "html.parser")
    #print soup
    for aid in soup.find_all('div', class_='ContentItem AnswerItem'):
        ansid = aid.get('name')
        getpage(questionid, ansid)

# 解析网页，得到图片的URL，调用下载模块 need to login.
def getpage(memberid):
    pageurl = u"https://www.douban.com/people/%s/statuses" % (memberid)  # 获取页面地址
    print(pageurl)
    session = requests.session()
    html = session.get(pageurl, headers=headers)
    print(html)
    # 返回网页内容
    soup = BeautifulSoup(html.content, "html.parser")
    print(soup)
    #print(soup.find_all('a'))
    for asrc in soup.find_all('a', class_="view-large"):
        print("something")
        pageurl = asrc.get('href')
        print(pageurl)
        #downpic(pageurl, soup.find_all('a', class_="view_large").index(asrc))

# 下载图片
def downpic(img_src, memberid, picname):
    global picnum
    CurrentPath = os.getcwd()
    if not os.path.exists("douban_statuses\%s_image" % memberid):
        os.makedirs("douban_statuses\%s_image" % memberid)
    filename = CurrentPath + u"\\douban\%s_image\%s.jpg" % (memberid, picname)
    picnum = picnum + 1
    print( "-----------------")
    print( img_src)
    print( filename)
    print( u'下完了%s张' % picnum)
    print( "-----------------")
    try:
        urllib.request.urlretrieve(img_src, filename)
    except Exception:
        print(u'这张图片下载出问题了： %s' % filename)


# 程序入口
if __name__ == '__main__':
    page = 0
    member_id = "91886435"
    #answer_id = "201250070"
user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
headers = {'User-Agent': user_agent, 'Referer': 'http://douban.com'}
# 准备headers
pagenum = 0
picnum = 0
# 准备计次变量
getpage(member_id)
