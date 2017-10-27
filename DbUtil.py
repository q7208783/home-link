# coding=UTF-8
import MySQLdb
import House

conn = MySQLdb.connect(host = "rm-wz92xoj923k8s3v8do.mysql.rds.aliyuncs.com",
                       port = 3306,
                       user = "root",
                       passwd ="Zc57198083",
                       db = "link-home",
                       charset="utf8")
cur = conn.cursor()



def testdb():
    cur.execute("SELECT VERSION()")
    data = cur.fetchone()
    print "Database connect success! Database version : %s " % data

def saveToDatabase(House):

    return
