# coding=UTF-8
import sys
import time
import requests;
from lxml import html

from DbUtil import saveToDatabase
from House import House

url = "https://cd.lianjia.com/ershoufang/squre/co32ng1hu1nb1ba65ea10000ep10000/"
shuangliu = 'shuangliu'
tianfuxinqu = 'tianfuxinqu'


reload(sys)                         # 2
sys.setdefaultencoding('utf-8')

def get_houselist(squre):
    page = requests.get(url.replace('squre', squre))
    tree = html.fromstring(page.content.decode('UTF-8'))
    return tree.xpath("//div[4]/div[1]/ul/li")


def getHouse(house):
    price = int(house.xpath('./div[1]/div[6]/div[1]/span/text()')[0])
    url = str(house.xpath('./a/@href')[0])
    district = str(house.xpath('./div[1]/div[2]/div/a/text()')[0])
    structure = str(house.xpath('./div[1]/div[2]/div/text()')[0])
    unitPrice = str(house.xpath('./div[1]/div[6]/div[2]/span/text()')[0])
    return House(price, url, district, structure,unitPrice)


def save(house,squre):
    return saveToDatabase(house.price, house.url, house.district, house.structure,house.unitPrice,squre)


while True:
    for house in get_houselist(tianfuxinqu):
        houseObj = getHouse(house)
        if houseObj.price<125:
            save(houseObj,'天府新区')

    time.sleep(3)

    for house in get_houselist(shuangliu):
        houseObj = getHouse(house)
        if houseObj.price<115:
            save(houseObj,'双流')

    time.sleep(3)