# -*- coding: utf-8 -*-

import requests


from .. import wh
from . import wh_setting

def read(org_id="std"):
    api = "/api/org/%s/read"%(org_id)
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