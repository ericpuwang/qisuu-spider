#! /bin/python
# coding: utf-8

from bs4 import BeautifulSoup
from threading import Thread
from urlparse import urljoin
from download.QisuuThread import Downloader
from storage.mysql import MySQL
import threading

class Parser(Thread):
    '''
    BeautifulSoup
    获取每个页面上展示的所有小说
    '''
    root_url = 'https://www.qisuu.com'

    def __init__(self, content):
        self.content = content
        self.soup = BeautifulSoup(self.content, 'html.parser')
        self.stories = self.soup.find('div', {'class':'list'})
        self.mysql = MySQL('qisuu')

    def getPageNum(self):
        self.page_num = len(self.soup.find('select', {'name':'select'}).findAll('option'))

    def getAllStory(self):
        all_story = self.stories.findAll('li')
        for story in all_story:
            self.StoryDetail(story)

    def StoryDetail(self, story):
        relative_content_url = story.find('a')['href']
        relative_image_url = story.find('a').img['src']

        self.content_url = urljoin(self.root_url, relative_content_url)
        self.image_url = urljoin(self.root_url, relative_image_url)
        download_content = Downloader(self.content_url)
        download_content.start()
        download_content.join()

        self.parserDetail(download_content.context)
        sql = ('INSERT INTO story(name, content_url, image_url, size, author) '
            'VALUES({name}, {content_url}, {image_url}, {size}, {author})').format(
                name = self.name,
                content_url=self.content_url,
                image_url=self.image_url,
                size=self.size,
                author=self.author,
            )
        self.mysql.insert(sql)

    def run(self):
        self.getAllStory()

    '''
    获取小说的具体信息
    '''
    def parseDetail(self, content):
        if not content:
            return

        soup = BeautifulSoup(content, 'html.parser')
        info = self.soup.find('div', {'class':'detail_right'})
        self.name = self.info.h1.text
        self.size = self.info.ul.findAll('li')[3].text.split(u'：')[1]
        self.author = self.info.ul.findAll('li')[5].text.split(u'：')[1]