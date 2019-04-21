from lxml import etree
from complain.public import get_parse1, items
from complain import config
from complain.connection import set_url, check_url, conn_recall
from complain.log_decorator import Logger
log = Logger()

def get_urls(html):
    h = etree.HTML(html)
    urls = h.xpath("//div[@class='box_main']/div/div/ul/li/span/a/@href")
    return urls

def get_next_url(html):
    h = etree.HTML(html)
    next = h.xpath("//div[@class='page']/a[last() -1]/text()")
    print(next)
    if next != "下一页":
        return None
    srt = h.xpath("//div[@class='page']/a[last() -1]/@href")[0]
    url = config.recall4_url + str
    return url

def get_content(html, url):
    h = etree.HTML(html)
    s = h.xpath("//table/tbody/tr/td/br/../..")
    item_list = []
    for i in s:
        item = items()
        item['car_link'] = url
        # item['car_link'] = url
        item['car_series'] = ''.join(i.strip() for i in i.xpath("./td[1]/text()"))
        item['car_type'] = ''.join(i.strip() for i in i.xpath("./td[2]/text()"))[:45]
        item['brand'] = ''.join(i.strip() for i in h.xpath("//div[@class='table']/table/tbody/tr[1]/td[2]/text()"))
        item['title'] = ''.join( i.strip() for i in h.xpath("//div[@class='show_tit']/h1/text()"))
        start_time = h.xpath("normalize-space(//div[@class='show_tit2']/text())")
        if start_time:
            item['start_time'] = start_time.split('：')[1][:10] if '：' in start_time else start_time[:10]
        item['car_content'] = ''.join(i.strip() for i in h.xpath("//table/tbody/tr/td[contains(text(), '缺陷描述')]/..//text()"))
        item['source'] = '国家市场监督管理总局'
        item_list.append(item)
    return item_list

def main():
    for i in range(44,59):
        log.info('正在抓取第%d页'%(i))
        url = 'http://www.dpac.gov.cn/qczh/gnzhqc/index_%d.html'%i
        log.info('url:%s'%url)
        html = get_parse1(url)
        urls = get_urls(html)
        print(urls)
        str = 'http://www.dpac.gov.cn/qczh/'
        for url in urls:
            s = '/'.join(url.split('/')[1:])
            url = str + s
            # if check_url(url) is None:

            my_html = get_parse1(url)
            # print(my_html.decode('utf-8'))
            result = get_content(my_html, url)
            log.info(url)
            conn_recall(result)
            log.info(result)
                # set_url(url)
            # else:
            #     print('此链接已抓取过:',url)



if __name__ == '__main__':
    main()