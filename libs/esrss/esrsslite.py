#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from xml.etree.ElementTree import Element, tostring

class esRss:
    '''
    RSS lite generator class by Evgeniy Shumilov <evgeniy.shumilov@gmail.com>
    '''
    def __init__(self, title, link='', description='', language='ru', copyright='', image_url='', image_title='',
                 image_link='', managingEditor='', lastBuildDate=''):
        self.root = Element('rss')
        self.root.set('version', '2.0')
        self.channel = Element('channel')
        self.root.append(self.channel)
        for k in ('title', 'description', 'link', 'language'):
            if eval(k):
                tmpelem = Element(k)
                tmpelem.text = eval(k)
                self.channel.append(tmpelem)
            else:
                self.__err__('Feed should contain ' + k)
        for k in ('copyright', 'managingEditor', 'lastBuildDate'):
            if eval(k):
                tmpelem = Element(k)
                tmpelem.text = eval(k)
                self.channel.append(tmpelem)
        count = 0
        if image_url:
            tmpelem = Element('image')
            tmpelem2 = Element('url')
            tmpelem2.text = image_url
            tmpelem.append(tmpelem2)
            if image_title:
                tmpelem2 = Element('title')
                tmpelem2.text = image_title
                tmpelem.append(tmpelem2)
            if image_link:
                tmpelem2 = Element('link')
                tmpelem2.text = image_link
                tmpelem.append(tmpelem2)
            self.channel.append(tmpelem)

    def __err__(self, message='', code=0):
        if message:
            sys.stderr.write(message + '\n')
        if code:
            sys.exit(code)

    def addItem(self, title='', description='', link='', author='', category='', category_domain='', comments='',
                enclosure_url='', enclosure_length='', enclosure_type='', guid='', guid_isPermaLink='',
                pubDate='', source_url='', source_src=''):
        if title and description:
            item = Element('item')
            for k in 'title', 'description', 'link', 'author', 'comments', 'pubDate':
                tmpelem = Element(k)
                tmpelem.text = eval(k)
                item.append(tmpelem)
            if enclosure_url:
                tmpelem = Element('enclosure')
                tmpelem.set('url', enclosure_url)
                if enclosure_length:
                    tmpelem.set('length', enclosure_length)
                if enclosure_type:
                    tmpelem.set('type', enclosure_type)
                item.append(tmpelem)
            if category:
                tmpelem = Element('category')
                if category_domain:
                    tmpelem.set('domain', category_domain)
                    tmpelem.text = category
                item.append(tmpelem)
            if guid:
                tmpelem = Element('guid')
                if guid_isPermaLink:
                    tmpelem.set('isPermaLink', guid_isPermaLink)
                    tmpelem.text = guid
                item.append(tmpelem)
            if source_url:
                tmpelem = Element('source')
                if source_src:
                    tmpelem.text = source_src
                tmpelem.set('url', source_url)
                item.append(tmpelem)
            self.channel.append(item)
        else:
            self.__err__('Item should contain title or description')

    def Feed(self):
        return '<?xml version="1.0" encoding="UTF-8" ?>' + tostring(self.root)