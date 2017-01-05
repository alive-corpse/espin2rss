#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Microservice for rss feed from pinterest
"""

import re
import sys
import urllib2
from libs.esrss.esrsslite import esRss
import libs.server.bottle as bottle
import libs.server.wsgiserver as wsgiserver

route = bottle.route
response = bottle.response
static = bottle.static_file

if len(sys.argv) >= 3:
    if sys.argv[2]:
        host = sys.argv[2]
    else:
        host = 'localhost'
else:
    host = 'localhost'
if len(sys.argv) >= 2:
    if sys.argv[2]:
        port = int(sys.argv[1])
    else:
        port = 8080
else:
    port = 8080


def getContent(url):
    if url:
        resp = urllib2.urlopen(url)
        return resp.read().replace('\n', '')
    else:
        return ''

def getTitle(content):
    if content:
        return re.findall('<meta property="og:title" name="og:title" content="(.+?)" data-app>', content)[0].decode('UTF-8')
    else:
        return {}

def getDescription(content):
    if content:
        return re.findall('<meta property="twitter:description" name="twitter:description" content="(.+?)" data-app>',
                          content)[0].decode('UTF-8')
    else:
        return {}

def getPins(content):
    if content:
        lst = re.findall('title="(.+?)".+?srcset="(.+?)".*?href="(.+?)"', content)
        res = []
        for i in lst:
            res.append({'title': i[0].decode('UTF-8'), 'img': i[1].split(' ')[-2], 'url': i[2]})
        return res
    else:
        return []

@route('/<author>/<desk>')
def getRss(author, desk):
    if author and desk:
        url = 'https://ru.pinterest.com/%s/%s/' % (author, desk)
        content = getContent(url)
        rss = esRss(title=getTitle(content), link=url, description=getDescription(content))
        pins = getPins(content)
        for p in pins:
            description = "<h3>%s</h3><br><br><a href=\"%s\"><img src=\"%s\"></a>" % (p['title'], p['url'], p['img'])
            rss.addItem(title=p['title'], description=description, link=p['url'], guid=p['url'],
                        guid_isPermaLink='true')
        response.headers['Content-Type'] = 'xml/application'
        return rss.Feed()
    else:
        response.headers['Content-Type'] = 'text/plain'
        return 'Empty request'


bottle.debug(False)
wsgiapp = bottle.default_app()
httpd = wsgiserver.Server(wsgiapp, listen=host, port=port)
httpd.listen = host
httpd.port = port
httpd.serve_forever()
