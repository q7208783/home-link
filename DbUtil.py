from twisted.enterprise import adbapi              #导入twisted的包
import MySQLdb
import MySQLdb.cursors

def saveToDatabase(price, url, district, structure,unitPrice,squre):
    return