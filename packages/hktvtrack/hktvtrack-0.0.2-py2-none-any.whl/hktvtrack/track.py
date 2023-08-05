# -*- coding: UTF-8 -*-
import requests
import json
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def getProductStatus(code):
    #print("https://www.hktvmall.com/p/"+code)
    result = requests.get("https://www.hktvmall.com/p/"+code)
    c = result.content

    soup = BeautifulSoup(c, "html.parser")
    nametitle = soup.find("h1", {"class": ["last"]})

    for item in soup.findAll("div", {"class": ["buttonWrapper"]}):
        if item.text.strip() == '加入購物車':
            a = {'name': nametitle.text,  'isBuy': True}
            python2json = json.dumps(a, ensure_ascii=False)
            return python2json
        else:
            a = {'name': nametitle.text, 'isBuy': False}
            python2json = json.dumps(a, ensure_ascii=False)
            return python2json

#print(getProductStatus('H0888001_S_P10021200'))