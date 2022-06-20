import random

import requests


# 年费状态更新
def patent_update(feibiao_cookie, update_cookie, update_token):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36 Edg/98.0.1108.43',
        'Cookie': feibiao_cookie
    }

    param = {
        'token': update_token,
        'host': '49.7.96.252',
        'port': '16819',
        'cookie': update_cookie,
        'app_no_like': '',
        's_state': ''
    }

    patent_update_url = 'http://www.ipfeibiao.com/manager/patentUpdateAnnualState/updatePatents'
    requests.post(url=patent_update_url, params=param, headers=headers)


# 年费采集更新
def annual_fee_to_update(feibiao_cookie, update_cookie, update_token, id):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.62',
        'Cookie': feibiao_cookie
    }
    param = {
        'id': id,
        'token': update_token,
        'host': '49.7.96.252',
        'port': '16819',
        'cookie': update_cookie
    }
    gather_url = 'http://www.ipfeibiao.com/manager/patentUpdateAnnualfee/getAnnualFeeById'

    response = requests.post(url=gather_url, params=param, headers=headers).text
    return response


# 获取年费状态更新专利号
def get_patent_number(feibiao_cookie):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36 Edg/98.0.1108.43',
        'Cookie': feibiao_cookie
    }
    param = {
        'page': 1,
        'limit': 20
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


# 获取专利年费采集专利号以及更新id(state为true获取ids)
def get_acquisition_patent_Number(feibiao_cookie, state):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36 Edg/98.0.1108.43',
        'Cookie': feibiao_cookie
    }
    param = {
        'page': 1,
        'limit': 90,
        'collection_state': 1
    }
    url = 'http://www.ipfeibiao.com/manager/patentUpdateAnnualfee/list'

    response = requests.post(url=url, params=param, headers=headers)
    list_data = response.json()

    # 专利年费采集更新数量
    annual_fee_quantity = list_data['count']

    # 获取年费采集更新id
    ids = []
    if state:
        for id in list_data['data']:
            ids.append(id['id'])
        return ids

    # 获取年费采集专利号
    patent_acquisition = []
    for id in list_data['data']:
        patent_acquisition.append(id['app_no'])

    return patent_acquisition


# 系统日志专利状态更新次数
def update_successfully(feibiao_cookie):
    """
    :param feibiao_cookie: 飞镖网cookie值
    :return: 系统日志专利状态更新次数
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36 Edg/98.0.1108.43',
        'Cookie': feibiao_cookie
    }
    param = {
        'page': 1,
        'limit': 50,
        'log_type': '专利状态'
    }

    url = 'http://www.ipfeibiao.com/manager/sysLog/list'

    response = requests.post(url=url, params=param, headers=headers)
    list_data = response.json()

    return list_data['count']
