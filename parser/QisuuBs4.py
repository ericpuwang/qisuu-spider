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
    root_url = 'https://www.qisuu.com'

    def __init__(self):
        self.current_info = _duplex_queue.leftpop()
        self.mysql = MySQL('qisuu')
        super(Parser, self).__init__()

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
        try:
            self.name = re.match(u'《?.+》', info.h1.text).group()[1:-1]
            self.size = info.ul.findAll('li')[1].text.split(u'：')[1]
            self.status = info.ul.findAll('li')[4].text.split(u'：')[1]
            self.author = info.ul.findAll('li')[5].text.split(u'：')[1]
        except:
            _duplex_queue.rightpush(self.url)
        else:
            relative_image_url = self.soup.find('div', {'class':'detail_pic'}).find('img')['src']
            self.image_url = urljoin(self.root_url, relative_image_url)
            info = '{0} {1} {2} {3} {4} {5}'.format(self.name, self.url, self.image_url, self.size, self.status, self.author)
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

        if re.match('index_\d+\.html', self.url.split('/')[-1]) or not self.url.split('/')[-1]:
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