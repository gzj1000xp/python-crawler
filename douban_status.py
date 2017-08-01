# -*- coding: utf-8 -*
import urllib
from bs4 import BeautifulSoup
import os
import requests
import re
import time
import json
import random


# 配置爬虫代理
def getproxy(ip_pool_url):
    ip_url = requests.get(ip_pool_url)
    ip_url_bs = BeautifulSoup(ip_url.content, "html.parser")
    ip_list = json.loads(str(ip_url_bs))
    proxy_ip = random.choice(ip_list)[0]
    proxy_port = random.choice(ip_list)[1]
    proxy_add = "http://" + proxy_ip + ":" + str(proxy_port)
    print(proxy_add)
    return proxy_add

# 登录函数
def login(username, password, proxy_address):
    login_str = u'登录'
    data = {
        'source':'None',
        'form_email': username,
        'form_password':password,
        'login':login_str
    }
    login_url = 'https://www.douban.com/accounts/login'
    session = requests.session()
    html = session.get(login_url, headers=headers, proxies={'http': proxy_address}).text
    captcha_img_pattern = r'(?<=<img id="captcha_image" src=\").*?(?=\")'
    captcha_image_url = re.search(captcha_img_pattern,html,re.S|re.M|re.I)
    if captcha_image_url is not None:
        captcha_image_url = captcha_image_url.group()
        print(captcha_image_url)
        # captcha_image = session.get(captcha_image_url).text
        captcha_image = requests.get(captcha_image_url, headers=headers, proxies={'http': proxy_address}).content
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
    session.post(login_url, headers=headers, data=data, proxies={'http': proxy_address})
    print(data)
    print(session.cookies.items())
    return session

# 解析网页，得到图片的URL，调用下载模块 need to login.
def getpage(memberid, pageid, login_session, proxy_address):
    pageurl = u"https://www.douban.com/people/%s/statuses?p=%d" % (memberid, pageid)  # 获取页面地址
    print(pageurl)
    #session = requests.session()
    html = login_session.get(pageurl, headers=headers, proxies={'http': proxy_address})
    #print(html)
    # 返回网页内容
    soup = BeautifulSoup(html.content, "html.parser")
    #print(soup)
    #print(soup.find_all('a', class_="view-large"))
    for asrc in soup.find_all('a', class_="view-large"):
        pageurl = asrc.get('href')
        picname=pageurl.split('/')[-1]
        downpic(pageurl, memberid, picname)
    if pageid <= 10:
        pageid += 1
        print(pageid)
        #leastlink = pageurl
        getpage(memberid, pageid, login_session, proxy_address)
    else:
        pageid = pageid - 1
        print("共爬到%d页" % pageid)

# 下载图片
def downpic(img_src, memberid, picname):
    global picnum
    CurrentPath = os.getcwd()
    if not os.path.exists("douban_statuses\%s_image" % memberid):
        os.makedirs("douban_statuses\%s_image" % memberid)
    filename = CurrentPath + u"\\douban_statuses\%s_image\%s" % (memberid, picname)
    picnum = picnum + 1
    print( "-----------------")
    print( img_src)
    print( filename)
    print( u'下完了%s张' % picnum)
    print( "-----------------")

    #requests.get(img_src, filename, proxies={'http': proxy_address})
    proxy = urllib.request.ProxyHandler({'http': proxy_address})
    opener = urllib.request.build_opener(proxy)
    urllib.request.install_opener(opener)
    urllib.request.urlretrieve(img_src,filename)

    #urllib.request.urlretrieve(img_src, filename, proxies={'http': proxy_address})
    time.sleep(1)

'''  
    if not os.path.isfile(filename):
        try:
            urllib.request.urlretrieve(img_src, filename, proxies={'http': proxy_address})
            time.sleep(1)
        except Exception:
            print(u'这张图片下载出问题了： %s' % filename)
'''
# 程序入口

page = 0
member_id = "91886435"
#user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
#headers = {'User-Agent': user_agent, 'Referer': 'http://douban.com'}
# 准备headers
pagenum = 0
picnum = 0
# 准备计次变量

username = 'yixi1993@hotmail.com'
password = 'woshigzj'
ip_pool_url = "http://60.205.220.209:8000/?types=0&count=50&country=国内"
proxy_address = getproxy(ip_pool_url)

headers = {
    "Host": "www.douban.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.6",
    "Accept-Encoding": "gzip, deflate, sdch, br",
    "Connection": "keep-alive"
}
login_session = login(username, password, proxy_address)
getpage(member_id, 10, login_session, proxy_address)

