import re
import requests
import json
from lxml import etree
from bigDataGet.connection import conns, redis_get, redis_set
from bigDataGet.public import get_parse
from bigDataGet.log_decorator import loggerInFile

def get_url(html):
    if html is None:
        return None
    h = etree.HTML(html)
    items = h.xpath("//div[@class='kf_border']/div/div/h6")
    urls = []
    for item in items:
        html = etree.tostring(item, encoding='utf-8').decode()
        pattern = re.compile('<h6>.*?tanchu.*?(\d+).*?>.*?')
        num = pattern.findall(html)[0]
        str = 'http://www.qiche365.org.cn/index.php?m=all&c=index&a=info_complain&dat='
        urls.append(str + num)
    return urls

def get_next_url(html):
    h = etree.HTML(html)
    url = ''.join(i.strip() for i in h.xpath("//div[@class='kode-pagination']/a[last()]/@href"))
    return url

def get_content(html):
    if html is None:
        return None
    pattern = re.compile("<table.*?<td>(.*?)</td>.*?<td>.*?</td><td>(.*?)</td>.*?<td>.*?</td><td>(.*?)</td>.*?<td>.*?</td><td>(.*?)</td>.*?<td>.*?</td><td>(.*?)</td></tr></table>", re.S)
    item_list = pattern.findall(html)
    data = {}
    data['tc_numbers'] = ''
    data['brand'] = item_list[0][0]
    data['car_series'] = item_list[0][1]
    data['car_type'] = item_list[0][0]
    data['car_describe'] = item_list[0][4]
    data['car_question'] = item_list[0][2]
    data['start_time'] = item_list[0][3][:10]
    print(data)
    return data

def main():
    url = "http://www.qiche365.org.cn/index.php?m=all&c=complain&a=clist&page=1"
    while 1:
        if url:
            html = get_parse(url)
            urls = get_url(html)[:4]
            for url in urls:
                if redis_get(url) is None:
                    my_html = get_parse(url)
                    result = get_content(my_html)
                    if result:
                        if '北京' in result['brand'] or '北汽' in result['brand']:
                            print('result',result)
                            # conns(result)
                            # redis_set(url)
                else:
                    print('该url已抓去过:',url)
                    break
            url = get_next_url(html)
        else:
            print('抓取完毕')
            break

if __name__ == '__main__':
    main()