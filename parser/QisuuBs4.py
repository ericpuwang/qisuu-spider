#! /bin/python
# coding: utf-8

from bs4 import BeautifulSoup
from threading import Thread
from urlparse import urljoin
from queue.QisuuQueue import DuplexQueue
from storage.mysql import MySQL
import threading
import re

_duplex_queue = DuplexQueue()

class Parser(Thread):
    '''
    BeautifulSoup
    获取每个页面上展示的所有小说
    '''
    root_url = 'https://www.qisuu.com'

    def __init__(self):
        self.url = _duplex_queue.leftpop()['url']
        self.content = _duplex_queue.leftpop()['content']
        self.soup = BeautifulSoup(self.content, 'html.parser')
        self.mysql = MySQL('qisuu')

    def getPageNum(self):
        # 获取每种小说类型的展示页数
        self.page_num = len(self.soup.find('select', {'name':'select'}).findAll('option'))

    def run(self):
        self.parse()

    '''
    获取小说列表
    '''
    def _list(self):
        page_url = self.soup.find('div', {'class': 'tspage'})
        next_page_url = page_url.findAll('a')[-2]['href']
        if not next_page_url.endswith('index_1.html'):
            _duplex_queue.rightpush(urljoin(self.root_url, next_page_url))

        story_list = self.soup.find('div', {'class': 'list'}).findAll('li')
        for story in story_list:
            relative_content_url = story.find('a')['href']
            self.content_url = urljoin(self.root_url, relative_content_url)
            _duplex_queue.rightpush(self.content_url)

    '''
    获取小说的具体信息
    '''
    def _detail(self):
        info = self.soup.find('div', {'class':'detail_right'})
        self.name = info.h1.text
        self.image_url = None
        self.size = info.ul.findAll('li')[3].text.split(u'：')[1]
        self.author = info.ul.findAll('li')[5].text.split(u'：')[1]

    '''
    解析页面内容
    '''
    def parse(self):
        if re.match('index_\d+\.html', self.url.split('/')[-1]) or not self.url.split('/')[-1]:
            self._list()
        else:
            self._detail()

            sql = ('INSERT INTO story(name, content_url, image_url, size, author) '
                'VALUES({name}, {content_url}, {image_url}, {size}, {author})').format(
                    name=self.name,
                    content_url=self.content_url,
                    image_url=self.image_url,
                    size=self.size,
                    author=self.author,
                )
            self.mysql.insert(sql)