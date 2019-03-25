import json
from lxml import etree
from bigDataGet.public import get_parse
from bigDataGet.log_decorator import Logger
from bigDataGet.connection import conns, redis_get, redis_set
from bigDataGet.IPPool import IPPoolManager
log = Logger()

def get_unique_url(html):
    if html:
        url = ''.join(i.strip() for i in html.xpath("./td[5]/a/@href"))
        return url
    else:
        return None

def get_next_url(html):
    if html:
        h = etree.HTML(html)
        url = ''.join(i.strip() for i in h.xpath("//div[@class='p_page']/a[last()-1]/@href"))
        str = 'http://www.12365auto.com/zlts/'
        if url:
            return str + url
        else:
            return None
    else:
        return None

def get_content(html):
    if html is None:
        return None
    h = etree.HTML(html)
    items = h.xpath("//div[@class='tslb_b']/table")[0]
    data_list = []
    url_list = []
    x = 0
    for item in items:
        if x != 0:
            unique_url = get_unique_url(item)
            if redis_get(unique_url) is None:
                data = {}
                data['tc_numbers'] = ''.join(i.strip() for i in item.xpath("./td[1]/text()"))
                data['brand'] = ''.join(i.strip() for i in item.xpath("./td[2]/text()"))
                data['car_series'] = ''.join(i.strip() for i in item.xpath("./td[3]/text()"))
                data['car_type'] = ''.join(i.strip() for i in item.xpath("./td[4]/text()"))
                data['car_describe'] = ''.join(i.strip() for i in item.xpath("./td[5]/a/text()"))
                str = ''.join(i.strip() for i in item.xpath("./td[6]/text()"))
                s = ''
                for i in str.split(','):
                    value = i[:1]
                    id = i[1:]
                    with open('date.json', 'r', encoding='utf-8') as f:
                        for d in json.load(f):
                            if d['value'] == value:
                                for i in d['items']:
                                    if i['id'] == int(id):
                                        s = s + i['title']
                data['car_question'] = s
                data['start_time'] = ''.join(i.strip() for i in item.xpath("./td[7]/text()"))
                data['status'] = ''.join(i.strip() for i in item.xpath("./td[8]/em/text()"))
                data['source'] = '车质网'
                data_list.append(data)
                url_list.append(unique_url)
            else:
                log.info("此链接以及抓取过")
        x += 1
    print(data_list)
    return data_list, url_list

def main(pare):
    # url = "http://www.12365auto.com/zlts/272-0-0-0-0-0_0-0-0-1.shtml"
    urls = ["http://www.12365auto.com/zlts/272-0-0-0-0-0_0-0-0-1.shtml","http://www.12365auto.com/zlts/373-0-0-0-0-0_0-0-0-1.shtml","http://www.12365auto.com/zlts/371-0-0-0-0-0_0-0-0-1.shtml","http://www.12365auto.com/zlts/389-0-0-0-0-0_0-0-0-1.shtml","http://www.12365auto.com/zlts/11-0-0-0-0-0_0-0-0-1.shtml","http://www.12365auto.com/zlts/18-0-0-0-0-0_0-0-0-1.shtml","http://www.12365auto.com/zlts/305-0-0-0-0-0_0-0-0-1.shtml"]
    for url in urls:
        x = 0
        print('一类抓取完毕')
        while 1:
            if url:
                print(url)
                html = get_parse(url, pare)
                data_list, url_list = get_content(html)
                if data_list and url_list:
                    conns(data_list)
                    redis_set(url_list)
                    print(data_list)
                    print(url_list)
                else:
                    x += 1
                    if x > 3:
                        break
                url = get_next_url(html)
            else:
                break

if __name__ == '__main__':
    pool = IPPoolManager()
    pare = pool.get_ippool()
    main(pare)