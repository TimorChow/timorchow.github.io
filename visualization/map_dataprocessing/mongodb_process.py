import pymongo
import json


my_client = pymongo.MongoClient("mongodb://18.222.192.138:27017/")
my_db = my_client['51ca']
my_boundary = my_db['boundary']
my_assault = my_db['assault']
my_estate = my_db['estate']


def get_boundary(city_name):
    '''
    search a boundary coordinate of a given city

    :param city_name: str
    :return: list: contains boundary coordinate
    '''
    boundary = my_boundary.find_one({"city_name": city_name})['boundary']
    return boundary

def get_assault_coordinate():
    result = my_assault.find()
    item_list = [[item['lat'], item['lng']] for item in result]
    return item_list


def get_price_coordinate():
    """
    返回一个n*3 的 数组, [lat, lng, price] , price可要可不要
    :return:
    """
    result = my_estate.find()
    item_list = [[item['latitude'], item['longitude']] for item in result]
    print(len(item_list))
    return item_list

if __name__ == "__main__":
    print(json.dumps(get_price_coordinate()))
