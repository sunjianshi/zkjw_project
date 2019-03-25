import requests
from lxml import etree
from bigDataGet.log_decorator import Logger
from bigDataGet.connection import conns, redis_set, redis_get
from bigDataGet.public import get_parse

def get_url(html):
    h = etree.HTML(html)
    items = h.xpath("//tr[@class='purple']/td/a/@href")
    # print(items)
    urls = []
    for item in items:
        str = 'http://www.qctsw.com'
        urls.append(str + item)
    return urls

def get_next_url(html):
    h = etree.HTML(html)
    url = ''.join(i.strip() for i in h.xpath("//div[@class='endPageNum']/a[last()-1]/@href"))
    str = 'http://www.qctsw.com'
    if url is None:
        return None
    return str + url

def get_content(html):
    item = etree.HTML(html)
    data = {}
    data['tc_numbers'] = ''.join(i.strip() for i in item.xpath("//div[@class='tableBox']/table/tr[1]/td/b/text()"))
    data['brand'] = ''.join(i.strip() for i in item.xpath("//div[@class='tableBox']/table/tr[1]/td/a[1]/text()"))
    data['car_series'] = ''.join(i.strip() for i in item.xpath("//div[@class='tableBox']/table/tr[1]/td/a[2]/text()"))
    data['car_type'] = item.xpath("normalize-space(//div[@class='tableBox']/table/tr[2]/td[2]/text())")
    data['car_describe'] = item.xpath("normalize-space(//div[@class='articleContent']/p/text())")
    data['car_question'] = ''.join(i.strip() for i in item.xpath("//div[@class='articleContent']/table/tr[8]/td/p/a/b/text()"))
    data['start_time'] = item.xpath("normalize-space(//div[@class='tableBox']/table/tr[3]/td[1]/text())")
    status = item.xpath("normalize-space(//div[@class='end']/p/text())")
    if status:
        data['status'] = status.split("：")[1] if '：' in status else status
    else:
        data['status'] = ''
    data['source'] = '汽车投诉网'
    print(data)
    return data

def main():
    # url = "http://www.qctsw.com/tousu/tsSearch/252_0_0_0_0_0,0,0,0,0,0_0.html"
    urls = ["http://www.qctsw.com/tousu/tsSearch/252_0_0_0_0_0,0,0,0,0,0_0.html","http://www.qctsw.com/tousu/tsSearch/8_0_0_0_0_0,0,0,0,0,0_0.html","http://www.qctsw.com/tousu/tsSearch/12_0_0_0_0_0,0,0,0,0,0_0.html","http://www.qctsw.com/tousu/tsSearch/254_0_0_0_0_0,0,0,0,0,0_0.html","http://www.qctsw.com/tousu/tsSearch/175_0_0_0_0_0,0,0,0,0,0_0.html","http://www.qctsw.com/tousu/tsSearch/255_0_0_0_0_0,0,0,0,0,0_0.html"]
    for url in urls:
        x = 0
        while 1:
            if url:
                html = get_parse(url)
                if html:
                    urls = get_url(html)
                    print(urls)
                    data_list = []
                    url_list = []
                    for url in urls:
                        if redis_get(url) is None:
                            my_html = get_parse(url)
                            if my_html:
                                result = get_content(my_html)
                                data_list.append(result)
                                url_list.append(url)
                        else:
                            print('此链接已抓去过')
                    if data_list and url_list:
                        conns(data_list)
                        redis_set(url_list)
                        print(data_list)
                    else:
                        x += 1
                        if x > 3:
                            break
                    url = get_next_url(html)
                else:
                    print('url不能访问：',url)
                    break


if __name__ == '__main__':
    main()