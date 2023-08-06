# -*- coding: utf-8 -*-

import requests

from .. import wh
from . import wh_setting

def list():

    api = "/api/team/list"
    api_url = wh.Wh.url + api

    # param
    data = ""

    #cookies
    cookies = wh.Wh.whtoken

    # api호출
    result = requests.get(api_url, data=data, cookies=cookies)

    #결과확인
    result = wh_setting.result(result)
    return result


def user_list(team_idx):

    api = "/api/team/%s/user/list"%(team_idx)
    api_url = wh.Wh.url + api

    # param
    data = ""

    #cookies
    cookies = wh.Wh.whtoken

    # api호출
    result = requests.get(api_url, data=data, cookies=cookies)

    #결과확인
    result = wh_setting.result(result)
    return result