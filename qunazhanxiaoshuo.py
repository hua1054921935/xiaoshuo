# coding=utf-8# coding=utf-8
# 使用xpath写爬小说
import requests
import re
from lxml import etree
import json

class BookSpider:
    def __init__(self):
        # http: // www.cuiweiju88.com / modules / article / articlelist.php?class =0 & page=1

        self.start_url="http://www.cuiweiju88.com/modules/article/index.php?"
        self.headers= {"User-Agent": "Mozilla/5.0 (Macintosh; "
                             "Intel Mac OS X 10_7_0) "
                                 "AppleWebKit/535.11 (KHTML, like Gecko) "
                                 "Chrome/17.0.963.56 Safari/535.11"}
    def parse_url(self,url):
        response=requests.get(url,headers=self.headers)
        return response.content

    # 获取每页中每个小说的对应的url地址
    def get_content_list(self,content):
        html=etree.HTML(content)
        # 分组获取小说
        content_list=html.xpath('//table[@class="grid"]//tr')
        book_list=[]
        for i in range(1,len(content_list)):
            dict_content={}
            contents=content_list[i]
            dict_content['book_name']=contents.xpath('.//td[@class="odd"]/a/text()')
            dict_content['book_href']=contents.xpath('.//td[@class="odd"]/a/@href')
            dict_content['size']=contents.xpath('.//td[@class="even"]/text()')
            book_list.append(dict_content)
        return book_list

    # 4.获取每部小说的页面内容
    def get_book_content(self,book_list):
        content_list=[]
        for i in book_list:
            dict_content={}
            dict_content['book_name']=i['book_name']
            book_url=i['book_href']
            # print(book_url)
            dict_content['content']=self.parse_url(book_url[0])
            dict_content['start_url']=re.sub(r'index.html', "", book_url[0])
            content_list.append(dict_content)
        return content_list

    # 获取每部小说每章节对应的名字以及url
    def get_book_menu(self,content):
        html=etree.HTML(content)
        menu_list=html.xpath('//table[@id="at"]//tr')
        menus = []
        for i in range(0,len(menu_list)):

            menu=menu_list[i]
            small_menu_list=menu.xpath('./td')
            for i in small_menu_list:
                dict_menu = {}
                dict_menu['href']=i.xpath("./a/@href")
                dict_menu['href_name']=i.xpath("./a/text()")
                menus.insert(0,dict_menu)
            # print(menus)
        return menus

    # 获取每本书每章节对应的url并返回一个列表
    def get_menu_list(self,content_list):
        book_list=[]
        for i in content_list:
            dic_content={}
            dic_content['book_name']=i['book_name']
            dic_content['start_url']=i['start_url']
            content=i['content']
            dic_content['book_menu']=self.get_book_menu(content)
            # print(dic)
            book_list.append(dic_content)

        return book_list


    # 获取每本书的内容
    def get_one_book(self,book_list):
        for i in book_list:
            book_name=i['book_name']
            url=i['start_url']
            data=i['book_menu']

            with open(book_name[0]+'.txt','a') as f:
                data.reverse()
            # print(type(data.reverse()))
            for datas in data:
                print(type(datas['href_name'][0]))
                # f.write(str(json.dumps(datas['href_name'][0]))+'\n')
                # f.write(data+"\n")
                if len(datas['href'])!=0:
                    new_url=url+datas['href'][0]
                    content=self.parse_url(new_url)
                    html=etree.HTML(content)
                    data=html.xpath("//dd[@id='contents']/text()")
                    for datas in data:
                        ldata=json.dumps(datas,ensure_ascii=False)
                        f.write(ldata)
                    # f.write(data)


    def run(self):
        page=1
        url = self.start_url + str(page)
        # while True:
        # 1.获取url地址
        # 2.发出请求，获取数据
        content=self.parse_url(url)
        # 3. 数据处理,获取每页的小说名称和url
        book_list=self.get_content_list(content)
        # 4.获取每部小说的目录以及每章的url
        content_list=self.get_book_content(book_list)
        # 5.获取
        book_list=self.get_menu_list(content_list)
        data=self.get_one_book(book_list)

        # 5.获取下一页的url地址
            #循环2-5


if __name__ == '__main__':
    a=BookSpider()
    a.run()