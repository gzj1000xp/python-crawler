# -*- coding: utf-8 -*
import urllib
from bs4 import BeautifulSoup
import os
import requests
import re
import time


def login(username, password):
    login_str = u'登录'
    data = {
        'source':'None',
        'form_email': username,
        'form_password':password,
        'login':login_str
    }
    login_url = 'https://www.douban.com/accounts/login'
    session = requests.session()
    html = session.get(login_url, headers=headers).text
    captcha_img_pattern = r'(?<=<img id="captcha_image" src=\").*?(?=\")'
    captcha_image_url = re.search(captcha_img_pattern,html,re.S|re.M|re.I)
    if captcha_image_url is not None:
        captcha_image_url = captcha_image_url.group()
        print(captcha_image_url)
        # captcha_image = session.get(captcha_image_url).text
        captcha_image = requests.get(captcha_image_url, headers=headers).content
        document = 'login_captcha_douban.jpg'
        file_ = open(document, 'wb')
        file_.write(captcha_image)
        file_.close()
        captcha_solution = input('captcha_solution:')
        data['captcha-solution'] = captcha_solution
        # 获取captcha_id
        captcha_id_pattern = r'(?<=<input type="hidden" name="captcha-id" value=\").*?(?=\"/>)'
        captcha_id = re.search(captcha_id_pattern, html, re.S | re.M | re.I)
        if captcha_id is None:
            print('captcha_id error')
        else:
            captcha_id = captcha_id.group()
            data['captcha-id'] = captcha_id
    session.post(login_url, headers=headers, data=data)
    print(data)
    print(session.cookies.items())
    return session

# 解析网页，得到相册列表
def getalbum(memberid, pageid, login_session):
    pageurl = u"https://www.douban.com/people/%s/photos?start=%d" % (memberid, pageid)  # 获取页面地址
    #print(pageurl)
    # session = requests.session()
    html = login_session.get(pageurl, headers=headers)
    # print(html)
    # 返回网页内容
    soup = BeautifulSoup(html.content, "html.parser")
    #print(soup)
    for asrc in soup.find_all('a', class_="album_photo"):
        albumurl = asrc.get('href')
        album_name = albumurl.split('/')[-2]
        #print(albumurl)
        #print(album_name)
        getpage(albumurl, 0, login_session, album_name)


# 解析网页，得到图片页的URL
def getpage(albumurl, pageid, login_session, album_name, leastlink=360):
    pageurl = albumurl + "?start=%d" % (pageid)  # 获取页面地址
    print(album_name)
    #session = requests.session()
    html = login_session.get(pageurl, headers=headers)
    #print(html)
    # 返回网页内容
    soup = BeautifulSoup(html.content, "html.parser")
    #print(soup)
    #print(soup.find_all('a', class_="photolst_photo"))
    for asrc in soup.find_all('a', class_="photolst_photo"):
        pageurl = asrc.get('href')
        pageurl = pageurl + "large"
        #print(pageurl)
        getphoto(pageurl, login_session, album_name)
    if pageid < leastlink:
        pageid += 18
        print(pageid)
        #leastlink = pageid
        getpage(albumurl, pageid, login_session, leastlink)

# 解析网页，得到图片的URL，调用下载模块
def getphoto(pageurl, login_session, album_name):
    html = login_session.get(pageurl, headers=headers)
    soup = BeautifulSoup(html.content, "html.parser")
    #print(soup.find_all('img'))
    for asrc in soup.find_all('img'):
       photourl = asrc.get('src')
       if "view" in photourl:
           #print(photourl)
           picname = photourl.split('/')[-1]
           downpic(photourl, album_name, picname)

# 下载图片
def downpic(img_src, album_name, picname):
    global picnum
    CurrentPath = os.getcwd()
    #print(album_name)

    if not os.path.exists("douban_statuses\Album%s" % album_name):
        os.makedirs("douban_statuses\Album%s" % album_name)
    filename = CurrentPath + u"\\douban_statuses\Album%s\%s" % (album_name, picname)
    picnum = picnum + 1
    print( "-----------------")
    print( img_src)
    print( filename)
    print( u'下完了%s张' % picnum)
    print( "-----------------")

    if not filename:
        try:
            urllib.request.urlretrieve(img_src, filename)
            time.sleep(0.5)
        except Exception:
            print(u'这张图片下载出问题了： %s' % filename)


# 程序入口
if __name__ == '__main__':
    page = 0
    member_id = "tiffanyscode"
    #answer_id = "201250070"
user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
headers = {'User-Agent': user_agent, 'Referer': 'http://douban.com'}
# 准备headers
pagenum = 0
picnum = 0
# 准备计次变量

username = 'yixi1993@hotmail.com'
password = 'woshigzj'

login_headers = {
    "Host": "www.douban.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.6",
    "Accept-Encoding": "gzip, deflate, sdch, br",
    "Connection": "keep-alive"
}
login_session = login(username, password)
print(login_session)
getalbum(member_id, 0, login_session)
#getpage(member_id, 3, login_session)
