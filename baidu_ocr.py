# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 10:28:33 2021

@author: hasee
"""
import config.baidu_aip_config as config
import cv2
from aip import AipOcr

client = AipOcr(config.BAIDU_APP_ID, config.BAIDU_API_KEY, config.BAIDU_SECRET_KEY)

 
def image2text(fileName):
    with open(fileName, 'rb') as fp:
        image = fp.read()
    dic_result = client.basicGeneral(image)
    res = dic_result['words_result']
    result = ''
    for m in res:
        result = result + str(m['words'])
    return result


if __name__ == '__main__':
    print(image2text("screen_shoot//event_title.png"))    