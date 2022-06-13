import random

import requests


def header(feibiao_cookie):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
        'cookies': feibiao_cookie
    }
    return headers


# 年费状态更新
def patent_update(feibiao_cookie, update_cookie, update_token):
    param = {
        'token': update_token,
        'host': '49.7.96.252',
        'port': '16819',
        'cookie': update_cookie,
        'app_no_like': '',
        's_state': ''
    }

    patent_update_url = 'http://www.ipfeibiao.com/manager/patentUpdateAnnualState/updatePatents'

    requests.post(url=patent_update_url, params=param, headers=header(feibiao_cookie))


# 获取年费状态更新专利号
def get_patent_number(feibiao_cookie):
    param = {
        'page': 1,
        'limit': 200
    }
    url = 'http://www.ipfeibiao.com/manager/patentUpdateAnnualState/list'

    response = requests.get(url=url, params=param, headers=header(feibiao_cookie))
    list_data = response.json()

    # 年费状态更新数量
    annual_fee_quantity = list_data['count']

    patent_gather = []
    for ids in list_data['data']:
        patent_gather.append(ids['app_no'])

    return random.choice(patent_gather)


# 获取专利年费采集专利号以及更新id(state为true获取ids)
def get_acquisition_patent_Number(feibiao_cookie, state):
    param = {
        'page': 1,
        'limit': 90,
        'collection_state': 1
    }
    url = 'http://www.ipfeibiao.com/manager/patentUpdateAnnualfee/list'

    response = requests.post(url=url, params=param, headers=header(feibiao_cookie))
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
    param = {
        'page': 1,
        'limit': 50,
        'log_type': '专利状态'
    }

    url = 'http://www.ipfeibiao.com/manager/sysLog/list'

    response = requests.post(url=url, params=param, headers=header(feibiao_cookie))
    list_data = response.json()

    return list_data['count']
