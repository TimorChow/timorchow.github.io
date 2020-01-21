import pymongo
import json
import numpy as np
import matplotlib.pyplot as plt
import mplleaflet
from matplotlib.collections import PolyCollection
my_client = pymongo.MongoClient("mongodb://18.222.192.138:27017/")
#my_client = pymongo.MongoClient("mongodb://10.122.15.69:27017/")
print('MongoDB Connection Success!')
my_db = my_client['51ca']
my_boundary = my_db['boundary']
my_assault = my_db['assault']
my_estate = my_db['estate']
my_year_price  = my_db['sales']

def get_boundary(city_name):
    '''
    search a boundary coordinate of a given city

    :param city_name: str
    :return: list: contains boundary coordinate
    '''
    boundary = my_boundary.find_one({"city_name": city_name})['boundary']
    return boundary

def get_assault():
    '''
    return a list, every item includes 2017, 2018........
    :return: list
    '''
    result = my_assault.find()
    item_list = [item for item in result]
    return item_list

def get_year_price():
    result = my_year_price.find()
    item_list = [item for item in result]
    return item_list
if __name__ == "__main__":
    boundary_list=get_boundary('toronto')
    boundary_list = [(boundary['lat'], boundary['lng']) for boundary in boundary_list]
    # print(boundary_list[0])

    boundary_list=np.asarray(boundary_list)

    boundary_list[:,[0,1]] = boundary_list[:,[1, 0]]
    print(len(boundary_list))
    boundary_list=boundary_list.reshape(1,1315,2)
    fig, ax = plt.subplots()
    coll = PolyCollection(boundary_list,facecolors='yellow',edgecolors='black')
    ax.add_collection(coll)
    #estate_info = my_estate.find()
    estate_info = my_estate.find({},{"price":1,'_id':0, 'city':1})
    estate_info_list = [estate for estate in estate_info]
    print("price of estate",estate_info_list)
    estate_np=np.asarray(estate_info_list)
    #print(estate_info_list[:100])
    price = get_year_price()
    #3.28
    price_list = [(price_l['averageSoldPrice'])for price_l in price]
    price_list = np.asarray(price_list)
    print(price_list.max())
    print(price_list.min())


    #plt.show()

    # graph show
    #ax.plot(boundary_list[:,0],boundary_list[:,1] ,'gs')  # fast repair
    #mplleaflet.show(tiles='cartodb_positron', path='pot_holes.html',)



