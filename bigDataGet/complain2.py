import os
import requests
from lxml import etree
from bigDataGet.log_decorator import loggerInFile

def get_parse(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'
    }
    # try:
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    if response.status_code == 200:
        return response.text
    # except:
    #     pass

def get_url(html):
    # print(html)
    h = etree.HTML(html)
    items = h.xpath("//dd[@class='cont_l']/ul/li/a/@href")
    # print(items)
    return items

def join_url(url):
    srtList = url.split('/')
    strList = [i for i in srtList if i != '..']
    url = '/'.join(strList)
    print('http://www.cqn.com.cn/' + url)
    return 'http://www.cqn.com.cn/' + url

def get_content(html):
    h = etree.HTML(html)
    title = h.xpath("normalize-space(//h1/text())")
    content = h.xpath("//div[@class='content']/p/text()")
    # item['title'] = sel.xpath('a[normalize-space(//text())]').extract()
    print(title)
    print(content)

def main():
    url = "http://www.cqn.com.cn/ms/node_22312.htm"
    html = get_parse(url)
    url = "http://www.cqn.com.cn/ms/node_22312_%d.htm"%x
    urls = get_url(html)[:3]
    print(urls)
    for url in urls:
        print(url)
        s = "http://www.cqn.com.cn/ms/"
        url = s + url
        my_html = get_parse(url)
        result = get_content(my_html)

if __name__ == '__main__':
    main()