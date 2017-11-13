# coding=UTF-8
import requests
import json

from common.LogMgr import LogMgr

showapi_appid = "49449"  # 替换此值
showapi_sign = "af5667a9884d4e5da962e3f98f441d09"  # 替换此值
url = "http://route.showapi.com/99-38"
params = {'showapi_appid': showapi_appid, 'showapi_sign': showapi_sign, 'content': ""}
logger_pinyin = LogMgr('pinyin.log')


def hanzi2pinyin(content):
    params['content'] = content
    try:
        response = requests.get(url, params=params, timeout=10)
    except Exception as e:
        logger_pinyin.error("ERROR: request pinyin api got error, detail: " + e)
    result = response.content
    result_json = json.loads(result, encoding="utf8")

    if result_json['showapi_res_code'] == 0:
        bodydict = result_json['showapi_res_body']
        data = bodydict['data']
        return data.encode('utf8').replace(' ', '')
    else:
        logger_pinyin.error(
            "ERROR: api return code : " + str(result_json['showapi_res_code']) + " api error msg : " + result_json[
                'showapi_res_error'])
