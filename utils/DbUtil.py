# coding=UTF-8
import MySQLdb
import datetime

from utils import pinyin_utils, logger_util

conn = MySQLdb.connect(host="rm-wz92xoj923k8s3v8do.mysql.rds.aliyuncs.com",
                       port=3306,
                       user="root",
                       passwd="Zc57198083",
                       db="link-home",
                       charset="utf8")
cur = conn.cursor()

insertList = {}

logger = logger_util.get_logger('dblog.log')


def testdb():
    cur.execute("SELECT VERSION()")
    data = cur.fetchone()
    print "Database connect success! Database version : %s " % data


def saveToDatabase(House):
    House.create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if (not insertList.has_key(House.url)):
        insertList[House.url] = House;
    if (len(insertList) > 10):
        insert_list_to_database(insertList)
        insertList.clear()
    return


def insert_list_to_database(insertList):
    insertSql = """insert into house(
                    city_no, district_no, area_no,
                    house_price, house_size, house_address, 
                    house_structure, house_url, house_orient,
                    elevator, img_url, attention_num,
                    visit_num, release_time, unit_price , create_time, title
                    ) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    args = get_insert_house_args(insertList)
    try:
        print ('execute before')
        cur.executemany(insertSql, args)
        print ('execute after')
        conn.commit()
    except Exception as e:
        print e
        conn.rollback()
    print '[insert_by_many executemany] total:', len(insertList)


def get_insert_house_args(insertList):
    args = []
    for house in insertList.values():
        res = query_squre_no(house.area_name, house.squre)
        args.append([res[2], res[1], res[0],
                     house.price, house.house_size, house.area_name,
                     house.house_structure, house.url, house.house_orient,
                     house.house_elevator, house.img_url, house.follower_num,
                     house.visit_num, house.release_time, house.unitPrice,
                     house.create_time, house.title])
    return args


def query_squre_no(area, squre):
    query_sql_name = """select area_no,district_no,city_no from area where area_name = '%s'""" % (area)

    try:
        cur.execute(query_sql_name)
        result = cur.fetchone()
        if result is None:
            area_no = insert_house_area(squre, area)
            query_sql_no = """select area_no,district_no,city_no from area where area_no = '%s'""" % (area_no)
            cur.execute(query_sql_no)
            result = cur.fetchone()
        return result
    except Exception as e:
        logger.debug(e.message)


def check_valid(url):
    query_sql = """select count(house_url) as result from house where house_url = '%s'""" % (url)
    try:
        cur.execute(query_sql)
        result = cur.fetchone()
        return True if result[0] <= 0 else False
    except Exception as e:
        print e
        print 'select * from house , house_url got ERROR!'


def insert_house_area(squre, area, city='cd'):
    query_city_no_sql = """select city_no from city where city_name_simple = '%s' """ % (city)
    query_squre_no_sql = """select district_no from district where district_name = '%s' """ % (squre)
    query_area_no_sql = """select area_no from area where area_name = '%s' """ % (area)

    try:
        cur.execute(query_city_no_sql)
        city_no = cur.fetchone()[0]
        cur.execute(query_squre_no_sql)
        squre_no = cur.fetchone()[0]
        cur.execute(query_area_no_sql)
        area_no = cur.fetchone()
        if area_no is None:
            return insert_area(area, squre_no, city_no)
    except Exception as e:
        logger.debug('select got error : ' + e.message)
        raise e


def insert_area(area_name, district_no, city_no):
    insert_area_sql = """insert into area(area_name,district_no,city_no,area_name_pinyin) values(%s,%s,%s,%s)"""
    area_name_pinyin = pinyin_utils.hanzi2pinyin(area_name)
    args = (area_name, district_no, city_no, area_name_pinyin)
    try:
        cur.execute(insert_area_sql, args)
        conn.commit()
        return int(cur.lastrowid)
    except Exception as e:
        conn.rollback()
        logger.debug('insert area got error : ' + e.message)
        raise e


def select_all_squre():
    select_all_sql = """select district_name_pinyin,district_name from district"""
    try:
        cur.execute(select_all_sql)
        return cur.fetchall()
    except Exception as e:
        logger.debug("select district got error")
