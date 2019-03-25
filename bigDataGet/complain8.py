import re
import requests
from lxml import etree
from bigDataGet.log_decorator import Logger
from bigDataGet.connection import conns, redis_get, redis_set
from bigDataGet.public import get_parse
log = Logger()

def get_post_url(url, pstart, brid):
    data = {
        'pstart': pstart,
        'name': 'brid',
        'brid': brid
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
    }
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        return response.text
    else:
        return None

def get_url(html):
    pattern = re.compile('<tbody.*?</tbody>',re.S)
    item = pattern.findall(html)
    pattern = re.compile('data-href="(.*?)">')
    urls = pattern.findall(item[0])
    return urls

def get_content(html):
    # print(html)
    item = etree.HTML(html)
    data = {}
    data['tc_numbers'] = item.xpath("//div[@class='content-info']/p[1]/text()")[0].split('：')[1]
    data['brand'] = item.xpath("//div[@class='content-info']/p[2]/text()")[0].split('：')[1]
    data['car_series'] = item.xpath("//div[@class='content-info']/p[3]/text()")[0].split('：')[1]
    data['car_type'] = item.xpath("//div[@class='content-info']/p[4]/text()")[0].split('：')[1]
    data['car_describe'] = ''.join(i.strip() for i in item.xpath("//div[@class='content']/p[2]/text()"))
    data['car_question'] = ''.join(i.strip() for i in item.xpath("//div[@class='post-heading']/h6/text()"))
    data['start_time'] = item.xpath("//div[@class='content-info']/p[5]/text()")[0].split('：')[1]
    # print(data)
    return data

def main():
    brid_list = [10015,10016,10017,10018,10019]
    url = "https://www.qichemen.com/complain.html"
    for brid in brid_list:
        pstart = 0
        log.info('开始爬取%d'%brid)
        while 1:
            log.info('第%d页'%(pstart+1))
            html = get_post_url(url, pstart, brid)
            data_list = []
            url_list = []
            if html:
                urls = get_url(html)
                if urls == []:
                    print('爬取完毕')
                    break
                for my_url in urls:
                    if redis_get(my_url) is None:
                        try:
                            my_html = get_parse(my_url)
                            data = get_content(my_html)
                            if data is None:
                                log.info('%d抓取完毕'%brid)
                                break
                        except:
                            data = {}
                        data_list.append(data)
                        url_list.append(my_url)
                    else:
                        log.info('此链接已抓取过')
                        break
                if data_list:
                #     conns(data_list)
                #     redis_set(url_list)
                    print(data_list)
                pstart += 1
            else:
                break




if __name__ == '__main__':
    main()