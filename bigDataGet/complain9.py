import re
import requests
from lxml import etree
from bigDataGet.log_decorator import Logger
from bigDataGet.connection import conns, redis_get, redis_set
from bigDataGet.public import get_parse
log = Logger()

def get_url(html):
    """
    获取下一层url的列表
    :param html:
    :return:
    """
    h = etree.HTML(html)
    urls = h.xpath("//div[@class='news-list mstghover']/ul/li/div/h3/a/@href")
    log.info(urls)
    return urls

def get_next_url(html):
    """
    获取下一页的url
    :param html:
    :return:
    """
    h = etree.HTML(html)
    url = ''.join(i.strip() for i in h.xpath("//div[@class='wrap']/div/div/a[@class='next']/@href"))
    if url is None:
        return None
    return url

def get_content(html):
    """
    匹配内容
    :param html:
    :return:
    """
    item = etree.HTML(html)
    data = {}
    str2 = item.xpath("//div[@class='news-con Fs14 pLR20']/ul/li/p//text()")
    if str2:
        car_type = str2[-1].split('：') if '：' in str2[-1] else None
        if car_type:
            data['brand'] = car_type[1]
            data['car_series'] = car_type[1]
            data['car_type'] = car_type[1]
        else:
            data['brand'] = ""
            data['car_series'] = ""
            data['car_type'] = ""
        data['car_describe'] = ''.join(i.strip() for i in item.xpath("//div[@class='news-con Fs14 pLR20']/p/text()"))
        data['start_time'] = str2[1][5:15]
        str = item.xpath("//h1/text()")[0]  # 标题由投诉问题和编号组成
        pattern = re.compile('(.*?)\(编号：(\d+)')
        str_list = pattern.findall(str)
        data['tc_numbers'] = str_list[0][1]
        data['car_question'] = str_list[0][0].split('：')[1] if '：' in str_list[0][0] else str_list[0][0]
    return data

def main():
    url = "http://www.zizhuauto.com/index-htm-caid-822/page-1.html"
    next = 0
    while 1:
        if url:
            html = get_parse(url)
            urls = get_url(html)
            for url in urls:
                print(url)
                if redis_get(url) is None: #检查次url是否已获取过
                    items = get_parse(url)
                    data = get_content(items)
                    if data:
                        if '北京' in data['brand'] or '北汽' in data['brand']:
                            log.info('data2:{}'.format(data))
                            # conns(list(data))
                            # redis_set(url)
                    else:
                        log.info('此链接没有数据：%s'%url)
                else:
                    next += 1
                    log.info('此链接已抓去过:%s'%url)
                    if next > 5:
                        break
            url = get_next_url(html)
        else:
            break

if __name__ == '__main__':
    main()