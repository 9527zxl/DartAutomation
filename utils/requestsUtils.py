import random

import requests


# 获取年费状态更新专利号
def get_patent_number(feibiao_cookie):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
        'cookies': feibiao_cookie
    }
    param = {
        'page': 1,
        'limit': 200
    }
    url = 'http://www.ipfeibiao.com/manager/patentUpdateAnnualState/list'

    response = requests.get(url=url, params=param, headers=headers)
    list_data = response.json()

    # 年费状态更新数量
    annual_fee_quantity = list_data['count']

    patent_gather = []
    for ids in list_data['data']:
        patent_gather.append(ids['app_no'])

    return random.choice(patent_gather)
