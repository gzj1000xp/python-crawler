# -*- coding: utf-8 -*
import urllib
from bs4 import BeautifulSoup
import os
import requests
import time

# 解析网页，得到图片的URL，调用下载模块
def getpage(questionid, answerid):
    pageurl = u"https://www.zhihu.com/question/%s/answer/%s" % (questionid, answerid)  # 获取页面地址
    session = requests.session()
    html = session.get(pageurl, headers=headers)
    # 返回网页内容
    soup = BeautifulSoup(html.content, "html.parser")
    for asrc in soup.find_all('noscript'):
        pageurl = asrc.find('img').get('data-original')
        downpic(pageurl, answerid, soup.find_all('noscript').index(asrc))

# 下载图片
def downpic(img_src, answerid, picname):
    global picnum
    CurrentPath = os.getcwd()
    if not os.path.exists("zhihu\%s_image" % answerid):
        os.makedirs("zhihu\%s_image" % answerid)
    filename = CurrentPath + u"\\zhihu\%s_image\%s.jpg" % (answerid, picname)
    picnum = picnum + 1
    print( "-----------------")
    print( img_src)
    print( filename)
    print( u'下完了%s张' % picnum)
    print( "-----------------")
    try:
        urllib.request.urlretrieve(img_src, filename)
        time.sleep(1)
    except Exception:
        print(u'这张图片下载出问题了： %s' % filename)


# 程序入口
if __name__ == '__main__':
    page = 0
    question_id = "39752484"
    answer_id = "197778987"
user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
headers = {'User-Agent': user_agent, 'Referer': 'http://zhihu.com'}
# 准备headers
pagenum = 0
picnum = 0
# 准备计次变量
getpage(question_id, answer_id)
