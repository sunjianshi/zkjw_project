import requests
from urllib.parse import urlencode
from complain.log_decorator import Logger
from complain.connection import conns,set_url, redis_get
log = Logger()

def get_link(url,page,stat):
    data = {
        'page': page,
        'stat': stat
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
    }
    response = requests.post(url, headers=headers, data=data)
    pdata = urlencode(data)
    url = url + pdata
    return response.json(), url

def get_content(items, stat):
    data_list = []
    for item in items:
        data = {}
        data['tc_numbers'] = item['id']
        data['brand'] = item['catalogname']
        data['car_series'] = item['catalogname']
        data['car_type'] = item['catalogname']
        data['car_describe'] = item['content']
        data['car_question'] = item['title'] or item['problem']
        data['start_time'] = item['adddate']
        if stat == 1:
            data['status'] = '未处理'
        else:
            data['status'] = '已解决'
        data['source'] = '中国汽车消费网'
        if data['tc_numbers']:
            data_list.append(data)
    return data_list

def main():
    page = 1
    url = "http://tousu.315che.com/che_v3/struts_tousu/page"
    for stat in range(1,3):
        while 1:
            log.info('page:%d'%page)
            items, url_ = get_link(url, page, stat)
            log.info(url_)
            if redis_get(url_) is None:
                data_list = get_content(items, stat)
                if data_list == []:
                    log.info('抓取完毕')
                    break
                for data in data_list:
                    if '北京' in data['brand'] or '北汽' in data['brand']:
                        s = []
                        s.append(data)
                        print('北京or北汽',s)
                        conns(s)
                set_url(url_)
            page += 1


if __name__ == '__main__':
    main()