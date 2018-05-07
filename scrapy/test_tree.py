#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from lxml import etree
from subprocess import call, Popen, check_output
from multiprocessing import Process
import gevent
import sys
import os

def get_job_links():
    main = "https://www.v2ex.com"
    mes = requests.get(main + "/?tab=jobs", proxies = proxies, headers=header)
    print mes
    element = etree.HTML(mes.text)
    #print(element.xpath("string()"))
    txt = element.xpath('//span[@class="item_title"]/a')
    job_links = []
    for i in txt:
        #print i.getparent().tag
        print i.text
        job_links.append(main + dict(i.attrib).values()[0])
    return job_links

def start_process(url_list):
    tasks = []
    for i in url_list:
        tasks.append(gevent.spawn(get_message,i))
    gevent.joinall(tasks)


def get_message(links):
    global job_comment
    mes = requests.get(links, proxies = proxies, headers=header)
    element = etree.HTML(mes.text)
    #print element.xpath('string()')
    title = element.xpath("//div[@class='box']/div[@class='header']/h1")
    print "**********************"
    title_name = str(title[0].text)
    print title_name
    #comment = element.xpath("//div[@class='topic_content']/div[@class='markdown_body']")
    comment = element.xpath("//div[@class='topic_content']")
    print "**********************"
    for i in comment:
        job_comment = str(i.xpath("string()").encode('utf-8'))
    #print "echo '{0}' > test/{1} 2>&1".format(job_comment, title_name)
    try:
        with open('test/{0}'.format(title_name), 'w') as f:
            f.write(job_comment)
    except IOError:
        with open('test/{0}'.format(os.path.split(links)[-1]), 'w') as f:
            f.write(job_comment)
    else:
        f.close()

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf8') 
    header = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip,deflate",
        "Accept-Language": "en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/6",
        "Referer": "https://www.v2ex.com/?tab=jobs"
    }
    job_links = get_job_links()
    print len(job_links)
    for i in range(5):
        p = Process(target=start_process, args=(job_links[10*i:10*i+10],))
        p.start()
