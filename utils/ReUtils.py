import re;


def getAllNumeric(str):
    return re.findall(r"\d+\.?\d*", str)


def getFirstNumeric(str):
    return getAllNumeric(str)[0]
