# -*- coding: utf-8 -*-

# This code shows an example of text translation from English to Simplified-Chinese.
# This code runs on Python 2.7.x and Python 3.x.
# You may install `requests` to run this code: pip install requests
# Please refer to `https://api.fanyi.baidu.com/doc/21` for complete api document

import requests
import random
import json
from hashlib import md5
from config import *
import openai
import os

# Set your own appid/appkey.
#

# appid = 'Set your appid'
# appkey = 'Set your appkey'



def make_md5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()


def is_chinese(string):
    """
    检查整个字符串是否包含中文
    :param string: 需要检查的字符串
    :return: bool
    """
    # 这是我要翻译的文本的内容
    for ch in string:
        if not u'\u4e00' <= ch <= u'\u9fff':
            return False
    return True


def trans(query):
    if is_chinese(query):
        prompt = f"请将下面的中文翻译成英文：{query}"
    else:
        prompt = f"请将下面的英文翻译成中文：{query}"

    try:
        # api_key从环境变量中获取
        api_key = os.getenv("OPENAI_API_KEY")

        # 打印出所有的环境变量
        print(os.environ)
        # json格式化展示出来
        print(json.dumps(dict(os.environ), indent=4))

        client = openai.OpenAI(api_key=api_key)  # 替换为你的 key
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        print("response:", response)    
        return response.choices[0].message.content.strip()
    except Exception as e:
        return str(e)



if __name__ == "__main__":
    print(trans("驱动器不能为空"))

