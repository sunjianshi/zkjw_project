import re
from lxml import etree
# from bigDataGet.complain9 import get_content
from bigDataGet.public import get_parse

url = "http://www.zizhuauto.com/archive-htm-aid-990538.html"
# url = "http://www.zizhuauto.com/archive-htm-aid-991235.html"
def get_content(html):
    """
    匹配内容
    :param html:
    :return:
    """
    item = etree.HTML(html)
    data = {}
    # str = item.xpath("//h1/text()")[0]  #标题由投诉问题和编号组成
    str = "现代全新途胜(编号：990538)"
    print(str)
    pattern = re.compile('(.*?)\(编号：(\d+)')
    str_list = pattern.findall(str)
    print(str_list)
    data['tc_numbers'] = str_list[0][1]
    data['car_question'] = str_list[0][0].split('：')[1] if '：' in str_list[0][0] else str_list[0][0]
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
    return data

html = get_parse(url)
print(get_content(html))
