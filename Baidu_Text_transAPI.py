# -*- coding: utf-8 -*-

# This code shows an example of text translation from English to Simplified-Chinese.
# This code runs on Python 2.7.x and Python 3.x.
# You may install `requests` to run this code: pip install requests
# Please refer to `https://api.fanyi.baidu.com/doc/21` for complete api document

import requests
import random
import json
from hashlib import md5

# Set your own appid/appkey.

appid = 'Set your appid'
appkey = 'Set your appkey'


def make_md5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()


def is_chinese(string):
    """
    检查整个字符串是否包含中文
    :param string: 需要检查的字符串
    :return: bool
    """
    for ch in string:
        if not u'\u4e00' <= ch <= u'\u9fff':
            return False
    return True


def trans(query):
    # For list of language codes, please refer to `https://api.fanyi.baidu.com/doc/21`
    if is_chinese(query):
        from_lang = 'zh'
        to_lang = 'en'
    else:
        print("字符是英文，翻译成中文")
        from_lang = 'en'
        to_lang = 'zh'
    try:
        endpoint = 'http://api.fanyi.baidu.com'
        path = '/api/trans/vip/translate'
        url = endpoint + path

        query = query

        # Generate salt and sign

        salt = random.randint(32768, 65536)
        sign = make_md5(appid + query + str(salt) + appkey)

        # Build request
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = {'appid': appid, 'q': query, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}

        # Send request
        r = requests.post(url, params=payload, headers=headers)
        result = r.json()
        print(result)
        res = result["trans_result"][0]["dst"]
        return str(res)
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    print(trans("驱动器不能为空"))

# # Show response
# print(json.dumps(result, indent=4, ensure_ascii=False))
