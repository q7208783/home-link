# coding=UTF-8
import MySQLdb
import datetime

conn = MySQLdb.connect(host="rm-wz92xoj923k8s3v8do.mysql.rds.aliyuncs.com",
                       port=3306,
                       user="root",
                       passwd="Zc57198083",
                       db="link-home",
                       charset="utf8")
cur = conn.cursor()

insertList = {}


def testdb():
    cur.execute("SELECT VERSION()")
    data = cur.fetchone()
    print "Database connect success! Database version : %s " % data


def saveToDatabase(House):
    House.create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if(not insertList.has_key(House.url)):
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
        res = query_squre_no(house.area_name)
        args.append([res[2], res[1], res[0],
                     house.price, house.house_size, house.area_name,
                     house.house_structure, house.url, house.house_orient,
                     house.house_elevator, house.img_url, house.follower_num,
                     house.visit_num, house.release_time, house.unitPrice,
                     house.create_time, house.title])
    return args


def query_squre_no(area):
    query_sql = """select area_no,district_no,city_no from area where area_name = '%s'""" % (area)
    # query_sql = """select * from area"""
    try:
        cur.execute(query_sql)
        result = cur.fetchone()
        return result
    except Exception as e:
        print e
        print 'select * from area got ERROR ! '


def check_valid(url):
    query_sql = """select count(house_url) as result from house where house_url = '%s'""" % (url)
    try:
        cur.execute(query_sql)
        result = cur.fetchone()
        return True if result[0] <= 0 else False
    except Exception as e:
        print e
        print 'select * from house , house_url got ERROR!'


def insert_house_area(city,squre,area):
    query_sql = """insert """

