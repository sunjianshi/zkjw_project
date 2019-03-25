import requests
from bigDataGet.log_decorator import Logger
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
        # print('response:', response.text)
        return response.text
    else:
        return None

brid_list = [10016, 10015]
url = "https://www.qichemen.com/1complain.html"
for brid in brid_list:
    pstart = 0
    log.info('完成一页')
    while 1:
        log.info('pstart:%s'%pstart)
        print('pstart',pstart)
        try:
            html = get_post_url(url, pstart, brid)
        except Exception as e:
            log.error(e)
        pstart += 1
