# coding=UTF-8
class House(object):
    def __init__(self, title, price, url, district_name, house_structure, house_size, house_orient, house_decoration,
                 house_elevator, unitPrice, img_url, follower_num, visit_num, release_time, building_info, area_name):
        self.title = title
        self.price = price
        self.url = url
        self.district_name = district_name
        self.house_structure = house_structure
        self.house_size = house_size
        self.house_orient = house_orient
        self.house_decoration = house_decoration
        self.house_elevator = house_elevator
        self.unitPrice = unitPrice
        self.img_url = img_url
        self.follower_num = follower_num
        self.visit_num = visit_num
        self.release_time = release_time
        self.building_info = building_info
        self.area_name = area_name
