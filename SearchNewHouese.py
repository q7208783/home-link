# coding=UTF-8
import sys
import time
import requests;
import ReUtils
from lxml import html
import Queue

import DbUtil
from House import House

url = "https://cd.lianjia.com/ershoufang/squre/co32ng1hu1nb1ba65ea10000ep10000/"
shuangliu = 'shuangliu'
tianfuxinqu = 'tianfuxinqu'

reload(sys)  # 2
sys.setdefaultencoding('utf-8')
DbUtil.testdb()


def get_houselist(squre):
    page = requests.get(url.replace('squre', squre))
    tree = html.fromstring(page.content.decode('UTF-8'))
    return tree.xpath("//div[4]/div[1]/ul/li")


def getHouse(house):
    price = int(house.xpath('./div[1]/div[6]/div[1]/span/text()')[0])
    url = str(house.xpath('./a/@href')[0])
    district_name = str(house.xpath('./div[1]/div[2]/div/a/text()')[0])

    house_structure_list = str(house.xpath('./div[1]/div[2]/div/text()')[0]).split('|')
    house_structure = house_structure_list[1]
    house_size = ReUtils.getFirstNumeric(house_structure_list[2])
    house_orient = house_structure_list[3]
    house_decoration = house_structure_list[4]
    if (len(house_structure_list) > 5):
        house_elevator = house_structure_list[5]
    else:
        house_elevator = "未知"

    unitPrice = ReUtils.getFirstNumeric(str(house.xpath('./div[1]/div[6]/div[2]/span/text()')[0]))
    img_url = str(house.xpath('./a/img/@src')[0])

    follow_info_list = str(house.xpath('./div[1]/div[4]/text()')[0]).split('/')
    follower_num = ReUtils.getFirstNumeric(follow_info_list[0])
    visit_num = ReUtils.getFirstNumeric(follow_info_list[1])
    release_time = follow_info_list[2]

    building_info = str(house.xpath('./div[1]/div[3]/div/text()')[0])
    area_name = str(house.xpath('./div[1]/div[3]/div/a/text()')[0])
    title = str(house.xpath('./div[1]/div[1]/a/text()')[0])
    return House(title, price, url, district_name, house_structure, house_size, house_orient, house_decoration,
                 house_elevator, unitPrice, img_url, follower_num, visit_num, release_time, building_info, area_name)


def save(house):
    # return DbUtil.saveToDatabase(house.title, house.price, house.url, house.district_name, house.house_structure,
    #                       house.house_size, house.house_orient, house.house_decoration,
    #                       house.house_elevator, house.unitPrice, house.img_url, house.follower_num, house.visit_num,
    #                       house.release_time, house.building_info, house.area_name, squre)
    return DbUtil.saveToDatabase(house)


while True:

    list = [20]
    queue = Queue(30)
    for house in get_houselist(tianfuxinqu):
        houseObj = getHouse(house)
        houseObj.squre =  '天府新区'

        if houseObj.price < 125:
            save(houseObj)

    time.sleep(3)

    for house in get_houselist(shuangliu):
        houseObj = getHouse(house)
        if houseObj.price < 115:
            save(houseObj, '双流')

    time.sleep(3)
