# coding=UTF-8
import platform
import sys
import time

import requests
from lxml import html
import traceback
from common.LogMgr import LogMgr
from model.House import House
from utils import DbUtil, ReUtils

url = "https://cd.lianjia.com/ershoufang/squre/co32ng1hu1nb1ba65ea10000ep10000/"
reload(sys)  # 2
sys.setdefaultencoding('utf-8')
DbUtil.testdb()

queues = [];
queuesDict = {}

os_name = platform.platform()
logger_home_link = LogMgr('home-link.log')

def get_houselist(squre):
    try:
        page = requests.get(url.replace('squre', squre))
    except Exception as e:
        logger_home_link.error("ERROR: request " + url + " got error, detail: " + e)
    tree = html.fromstring(page.content.decode('UTF-8'))
    if ('Linux' in os_name):

        return tree.xpath('/html/body/div[4]/div[1]/ul/li')
    else:

        return tree.xpath("//div[4]/div[1]/ul/li")


def getHouse(house, squre):
    try:
        price = float(house.xpath('./div[1]/div[6]/div[1]/span/text()')[0])
        url = str(house.xpath('./a/@href')[0])
        district_name = str(house.xpath('./div[1]/div[2]/div/a/text()')[0])

        house_structure_list = str(house.xpath('./div[1]/div[2]/div/text()')[0]).split('|')
        index = 0
        house_structure = house_structure_list[1]
        if '别墅' in house_structure:
            house_structure = house_structure + '|' + house_structure_list[2]
            index = 1
        house_size = ReUtils.getFirstNumeric(house_structure_list[2 + index])
        house_orient = house_structure_list[3 + index]
        house_decoration = house_structure_list[4 + index]
        if (len(house_structure_list) > 5 + index):
            house_elevator = house_structure_list[5 + index]
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
    except Exception as e:
        logger_home_link.error("ERROR: xpath format got error, detail:" + e)
    return House(title, price, url, district_name, house_structure, house_size, house_orient, house_decoration,
                 house_elevator, unitPrice, img_url, follower_num, visit_num, release_time, building_info, area_name,
                 squre)


def save(house):
    return DbUtil.saveToDatabase(house)


def squreAllHouse(squre):
    for house in get_houselist(squre):
        houseObj = getHouse(house, squreDict[squre])
        logger_home_link.debug("DEBUG: Get a house, title: " + houseObj.title)
        if DbUtil.check_valid(houseObj.url):
            save(houseObj)

from SqureMap import get_squre_dict

squreDict = get_squre_dict()
while True:
    for key in squreDict:
        try:
            squreAllHouse(key)
        except:
            error_msg = traceback.format_exc()
            logger_home_link.error(error_msg)
    time.sleep(4)
