#-*- coding:utf-8 -*-

import urllib2
from bs4 import BeautifulSoup
import time
import re

def get_html(url):
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36'};
    request= urllib2.Request(url,headers=headers);

    max_try_num=5
    new_respHtml=None
    for one_try in range(max_try_num):
        try:
            new_resp = urllib2.urlopen(request)
            new_respHtml=new_resp.read()
            break
        except:
            if one_try<=(max_try_num):
                continue
            else:
                print 'Cannot open the url!'
                break
    return new_respHtml

def main():
    url="http://tech.qq.com/"
    resp_html = get_html(url)

    check_num=0
    if resp_html:
        soup = BeautifulSoup(resp_html.decode('gb2312','ignore'))
        structdiv=soup.find("div",attrs={"id": "listZone"})
        for i in structdiv.find_all("div",attrs={"class": "Q-tpListInner"}):
            check_num+=1
            print '-----------------------------',check_num,'---------------------------------'
            temp=i.find("h3")
            title_temp=temp.find("a")
            news_title=title_temp.get_text()
            print "News Title:",news_title

            detail = i.find("a")
            news_url = detail.get("href");
            print "News Url: ",news_url
            
            img=i.find('img')
            img_url=img.get('src')
            print "News Image Url: ",img_url

            time_temp= i.find("span",attrs={"class": "aTime"})
            time_news=time_temp.get_text()
            print "Publish Time:",time_news

            abstract_temp= i.find("p")
            abstract=abstract_temp.get_text()
            print "Abstract :",abstract

            try:
                comment_temp= i.find("div",attrs={"class": "plBtn"})
                com = comment_temp.find("span")
                comment_num=com.get_text()

                url_list = comment_temp.get("onclick")
                url = re.search(r"open\('(?P<lianjie>.+)'\)",url_list)
                url2=url.group("lianjie")
                print "Comment Url :",url2
            except:
                comment_num=0
            print "Comment Number:",comment_num

            tag_list_temp = i.find("span",attrs={"class": "techTag"})
            a_temp=tag_list_temp.find_all("a")
            tag_num=0
            for tag_temp in a_temp:
                tag_num+=1
                tag=tag_temp.get_text()
                print 'Tag ',tag_num,' :',tag
    else:
        print u'腾讯网的首页代码获取失败，请再次尝试！'

    print "----------------------------------------------------"
    print "新闻爬取结束，本次共爬取新闻条数：",check_num
    
if __name__=="__main__":
    main()
