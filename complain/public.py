#!/user/bin/env python
# -*- coding: utf-8 -*-

import requests
from bigDataGet.IPPool import IPPoolManager


def get_parse1(url, pare = ''):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}
    if pare:
        proxies = pare.get()
        try:
            print(url)
            response = requests.get(url, headers=headers, proxies=proxies)

            if response.status_code == 200:
                # response.encoding = 'utf-8'
                return response.content
        except:
            print('该链接不能访问：',url)
            return None
    else:
        try:
            print(url)
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response.content
        except:
            print('该链接不能访问：',url)
            return None

def get_parse(url, pare = ''):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}
    if pare:
        proxies = pare.get()
        try:
            print(url)
            response = requests.get(url, headers=headers, proxies=proxies)

            if response.status_code == 200:
                # response.encoding = 'utf-8'
                return response.text
        except:
            print('该链接不能访问：',url)
            return None
    else:
        try:
            print(url)
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response.text
        except:
            print('该链接不能访问：',url)
            return None

def get_post_json(url):
    data = {
        'page': 3,
        'stat': 1
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
    }
    response = requests.post(url, headers=headers, data=data)
    print(response.json())
    return response.json()

def items():
    items = {
        'car_series': '',
        'car_type': '',
        'title': '',
        'car_content': '',
        'start_time': '',
        'status': '',
        'source': '',
        'brand': '',
        'car_link': '',
    }
    return items