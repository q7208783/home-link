# coding=UTF-8
import sys
import time
import logging

import requests;
from lxml import html

from MyQueue import *
from SqureMap import squreDict
from model.House import House
from utils import DbUtil, ReUtils

url = "https://cd.lianjia.com/ershoufang/squre/co32ng1hu1nb1ba65ea10000ep10000/"

reload(sys)  # 2
sys.setdefaultencoding('utf-8')
DbUtil.testdb()

queues = [];
queuesDict = {}


def get_houselist(squre):
    page = requests.get(url.replace('squre', squre))
    tree = html.fromstring(page.content.decode('UTF-8'))
    return tree.xpath("//div[4]/div[1]/ul/li")


def getHouse(house, squre):
    price = float(house.xpath('./div[1]/div[6]/div[1]/span/text()')[0])
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
                 house_elevator, unitPrice, img_url, follower_num, visit_num, release_time, building_info, area_name,
                 squre)


def save(house):
    logging.debug('save before')
    return DbUtil.saveToDatabase(house)


def squreAllHouse(squre):
    if queuesDict.has_key(squre):
        queue = queuesDict[squre]
    else:
        queue = MyQueue(40)
    for house in get_houselist(squre):
        houseObj = getHouse(house, squreDict[squre])
        if houseObj.url not in queue:
            queue.enqueue(houseObj.url)
            save(houseObj)
            if (queue.isfull()):
                queue.dequeue()
    queuesDict[squre] = queue


while True:
    for key in squreDict:
        logging.debug('enter while')
        squreAllHouse(key)
    time.sleep(3)
