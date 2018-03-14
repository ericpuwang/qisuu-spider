#! /bin/python
# coding: utf-8

from bs4 import BeautifulSoup
from threading import Thread
from urlparse import urljoin
from queue.QisuuQueue import DuplexQueue
from storage.mysql import MySQL
import threading
import Queue
import sys
import re

reload(sys)
sys.setdefaultencoding('utf-8')

_duplex_queue = DuplexQueue()

class Parser(Thread):
    '''
    BeautifulSoup
    获取每个页面上展示的所有小说
    '''

    def __init__(self):
        self.current_info = _duplex_queue.leftpop()
        self.mysql = MySQL('qisuu')
        super(Parser, self).__init__()

    def run(self):
        self.parse()

    '''
    获取小说列表
    '''
    def _list(self):
        try:
            page_link = self.soup.find('div', {'class':'pagelink', 'id':'pagelink'})
            next_page_url = page_link.find('a', {'class':'next'})['href']
            _duplex_queue.rightpush(next_page_url)
        except Exception, e:
            _duplex_queue.rightpush(self.url)

        story_list = self.soup.find('div', {'id': 'slist'}).findAll('div', {'class':'book_bg'})
        for story in story_list:
            self.content_url = story.a['href']
            _duplex_queue.rightpush(self.content_url)

    '''
    获取小说的具体信息
    '''
    def _detail(self):
        info = self.soup.find('div', {'id':'soft_info_para'})
        try:
            self.name = info.h1.text
            detail_info = info.find('div', {'class':'soft_info_r'})
            self.image_url = detail_info.img['src']
            items = detail_info.findAll('li')
            self.author = items[0].text.split(u'：')[1]
            self.size = items[1].text.split(u'：')[1]
            self.status = items[6].text.split(u'：')[1]
            self.type = None
        except:
            _duplex_queue.rightpush(self.url)
        else:
            relative_image_url = self.soup.find('div', {'class':'detail_pic'}).find('img')['src']
            self.image_url = urljoin(self.root_url, relative_image_url)
            self.type = self.soup.find('div', {'class': 'wrap position'}).findAll('a')[-2].text
            info = '{0};{1};{2};{3};{4};{5};{6}'.format(
                self.name, self.url, self.image_url, self.size,
                self.status, self.author, self.type
            )
            with open('./result', 'a+') as f:
                f.write(info)
                f.write('\n')
    '''
    解析页面内容
    '''
    def parse(self):
        if not self.current_info:
            return

        self.url = self.current_info['url']
        self.content = self.current_info['content']
        self.soup = BeautifulSoup(self.content, 'html.parser')

        if re.match('\d+\.html', self.url.split('/')[-1]):
            self._list()
        else:
            self._detail()
            '''
            sql = ('INSERT INTO story(name, content_url, image_url, size, author) '
                'VALUES({name}, {content_url}, {image_url}, {size}, {author})').format(
                    name=self.name,
                    content_url=self.content_url,
                    image_url=self.image_url,
                    size=self.size,
                    author=self.author,
                )
            self.mysql.insert(sql)
            '''