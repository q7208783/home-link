# coding=UTF-8
from utils import DbUtil

def get_squre_dict():
    squre_dict = {}
    res = DbUtil.select_all_squre()
    for squre in res:
        squre_name_py = squre[0].encode('utf-8')
        squre_name = squre[1].encode('utf-8')
        squre_dict[squre_name_py] = squre_name
    return squre_dict

