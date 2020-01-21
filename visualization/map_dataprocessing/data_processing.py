# coding:utf-8
import json
import pymongo
import threadpool
import requests

# YOUR_API_KEY = "AIzaSyD3bduGNl2aykdb_elYJxtVjB_CTFJhHE0"  # Joe
YOUR_API_KEY = "AIzaSyAYRTDkSXnWXwZcuaaQJD4xzgI568Y8k_4"     # Lyon

# my_client = pymongo.MongoClient("mongodb://localhost:27017/")
my_client = pymongo.MongoClient("mongodb://18.222.192.138:27017/")
my_db = my_client['51ca']
my_estate = my_db["estate"]


def data_clean():
    '''
    filter repeated items
    :return:
    '''
    added_items_id = []
    add_item_container = []

    # travel all sources
    for i in range(1, 14):
        with open("source/house_source{}.txt".format(i), 'r') as file:
            datas = file.readlines()
            for data in datas:
                data_list = json.loads(data)['data']
                for data in data_list:
                    listing_id = data["listingId"]
                    if listing_id not in added_items_id:
                        added_items_id.append(listing_id)
                        add_item_container.append(data)

    temp_container = []
    for i in range(0, len(add_item_container), 200):
        temp_container.append(add_item_container[i: i+200])
    print(len(temp_container))
    with open('filtered.txt', 'a') as filter_file:
        for datas in temp_container:
            filter_file.writelines(json.dumps(datas)+'\n')
        # add_item_container = []


def nearby_search(item):
    '''
    搜索附近的商家, 并储存到mongodb, 失败的储存到fail.txt文件
    search nearby bank or other given place,
    save it into database
    save fails items to fail.txt
    :param item:
    :return:
    '''
    # 当字段存在且不为空, 跳过, 否则继续爬
    # do a filter, if the field is exist and not null, pass.
    result = my_estate.find_one({'_id':item['_id']})
    if item['_type'] in result and len(result[item['_type']])!=0:
        print(item['listingId']+' '+item['_type']+' exist')
        return None

    args = {
        "latitude" : item['latitude'],
        "longitude" : item['longitude'],
        "radius" : item['radius'],
        "_type" : item['_type'],
        "keyword" : item['keyword'],
        "YOUR_API_KEY" : YOUR_API_KEY


    }
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&radius" \
          "={radius}&type={_type}&keyword={keyword}&key={YOUR_API_KEY}".format(**args)
    try:
        req = requests.get(url)
        print(url)
        result = json.loads(req.content)['results']

        # 将结果按搜索类型存储到字段
        data = {item['_type']: result}

        my_estate.update({'_id': item['_id']},
                            {'$set': data})

        print(item['listingId']+' '+item['_type']+' success')
        # mutex.release()

    except:
        with open('fail.txt', 'a+') as file:
            file.writelines(item['listingId']+'\n')
        print('Error:'+item['listingId'])


def get_nearby_and_save():
    '''
    根据类别关键字搜索地点附近的商家,银行,学校等
    given a place, search stores, banks and schools nearby
    using multithread
    :return:
    '''
    # 储存每条房产信息
    result = my_estate.find()
    items_list = [item for item in result]
    task_list = []

    # 分别搜索附近的银行, 商场等不同种类的商家
    # item = items_list[0]
    for item in items_list:
        # choose different type
        ['restaurant', 'bank', 'school', 'subway_station', 'bus_station']
        item['_type'] = 'school'
        item['radius'] = 1500
        item['keyword'] = ''
        task_list.append(item)

    # start thread
    pool = threadpool.ThreadPool(30)
    thread_requests = threadpool.makeRequests(nearby_search, task_list)
    [pool.putRequest(req) for req in thread_requests]
    pool.wait()


def save_estate_to_mongodb():
    '''
    数据导入到mongodb数据库
    save estate
    :return:
    '''

    items_list = []
    with open("source/filtered.txt", 'r+') as file:
        lines = file.readlines()
        for line in lines:
            for data in json.loads(line):
                data = {
                    "listingId": data["listingId"],
                    "price": data["price"],
                    "unitNumber": data["unitNumber"],
                    "streetAddress": data["streetAddress"],
                    "crossStreet": data["crossStreet"],
                    "community": data["community"],
                    "city": data["city"],
                    "bedrooms": data["bedrooms"],
                    "dens": data["dens"],
                    "bathrooms": data["bathrooms"],
                    "latitude": data["latitude"],
                    "longitude": data["longitude"],
                    "Url": data["Url"],
                }
                items_list.append(data)

    # 插入记录
    x = my_estate.insert_many(items_list)


    # 查找
    result1 = my_estate.find_one({"listingId":'N4327501'})
    result1 = my_estate.find()

    print(result1.count())
    items_list = [item for item in result1]
    print(items_list[0]['_id'])

    # 增加字段
    # data = {'test' : 'aaaa'}
    # mycollection.update({"listingId":'N4327501'},
    #                     {"$set":data})

    # result2 = mycollection.find_one({"listingId":'N4327501'})
    # print(result2)

    # 删除字段
    # mycollection.update({"listingId": 'N4327501'},
    #                     {"$unset": data})
    # result3 = mycollection.find_one({"listingId":'N4327501'})
    # print(result3)

    # 删除文档
    # mycollection.drop()


def save_location_to_mongodb():
    '''
    transfer location data from .txt file to database
    :return:
    '''
    myboundary=my_db['boundary']
    item_list = []
    city_names_list = ['markhanm', 'mississauga', 'oakville', 'richmondhill', 'toronto', 'vaughan']
    for city_name in city_names_list:
        file_name = 'source/location_'+city_name+'.txt'
        with open(file_name, 'r+') as location_file:
            data = json.loads(location_file.readlines()[0])
            item = {
                'city_name': city_name,
                'boundary': data['data']['boundary'][0]
            }
            print(json.dumps(item))
            item_list.append(item)
    myboundary.insert_many(item_list)


def geocoding_save_to_mongodb():
    '''
    transfer a given place to coordinate
    :return:
    '''
    my_assault = my_db['assault']
    address_list = my_assault.find()
    address_list = [address for address in address_list]

    pre_url = "https://maps.googleapis.com/maps/api/geocode/json?address={} Toronto&key={}"
    GEOCODE_API = "AIzaSyD3bduGNl2aykdb_elYJxtVjB_CTFJhHE0"

    # travel every place, send a request, get result
    for address in address_list:
        address_name = address['Name']
        url = pre_url.format(address_name, GEOCODE_API)
        req = requests.get(url)
        data = json.loads(req.content)
        # content = '''{ "results" : [ { "address_components" : [ { "long_name" : "Guildwood", "short_name" : "Guildwood", "types" : [ "neighborhood", "political" ] }, { "long_name" : "Scarborough", "short_name" : "Scarborough", "types" : [ "political", "sublocality", "sublocality_level_1" ] }, { "long_name" : "Toronto", "short_name" : "Toronto", "types" : [ "locality", "political" ] }, { "long_name" : "Toronto Division", "short_name" : "Toronto Division", "types" : [ "administrative_area_level_2", "political" ] }, { "long_name" : "Ontario", "short_name" : "ON", "types" : [ "administrative_area_level_1", "political" ] }, { "long_name" : "加拿大", "short_name" : "CA", "types" : [ "country", "political" ] } ], "formatted_address" : "Guildwood, Toronto, ON, 加拿大", "geometry" : { "bounds" : { "northeast" : { "lat" : 43.7589447, "lng" : -79.1725445 }, "southwest" : { "lat" : 43.7275121, "lng" : -79.21494469999999 } }, "location" : { "lat" : 43.752743, "lng" : -79.19277699999999 }, "location_type" : "APPROXIMATE", "viewport" : { "northeast" : { "lat" : 43.7589447, "lng" : -79.1725445 }, "southwest" : { "lat" : 43.7275121, "lng" : -79.21494469999999 } } }, "place_id" : "ChIJBT1fwa7a1IkRwtl10Ot4zo0", "types" : [ "neighborhood", "political" ] } ], "status" : "OK" }'''
        latitude = data['results'][0]['geometry']['location']['lat']
        longtitude = data['results'][0]['geometry']['location']['lng']
        data = {
            'lat': latitude,
            'lng': longtitude,
        }
        # save to mongodb
        my_assault.update({'_id': address['_id']},
                          {'$set': data})
        print(address['Number']+": "+address['Name']+" Success")


def save_sale_situation_to_mongodb():
    my_sales = my_db['sales']
    sales = json.loads("""[{ "groupByValue":"2017-12", "averageSoldPrice":733304, "medianSoldPrice":null, "maxSoldPrice":13000000, "minSoldPrice":83000, "averageListingPrice":751223, "medianListingPrice":null, "averageDom":27, "medianDom":null, "soldVolume":4711, "newListingVolume":null, "onMarketVolume":null }, { "groupByValue":"2017-08", "averageSoldPrice":735885, "medianSoldPrice":null, "maxSoldPrice":8350000, "minSoldPrice":76000, "averageListingPrice":752930, "medianListingPrice":null, "averageDom":25, "medianDom":null, "soldVolume":6215, "newListingVolume":null, "onMarketVolume":null }, { "groupByValue":"2018-01", "averageSoldPrice":738820, "medianSoldPrice":null, "maxSoldPrice":8400000, "minSoldPrice":97000, "averageListingPrice":757057, "medianListingPrice":null, "averageDom":31, "medianDom":null, "soldVolume":4121, "newListingVolume":null, "onMarketVolume":null }, { "groupByValue":"2017-07", "averageSoldPrice":746379, "medianSoldPrice":null, "maxSoldPrice":11632000, "minSoldPrice":127000, "averageListingPrice":759409, "medianListingPrice":null, "averageDom":21, "medianDom":null, "soldVolume":5906, "newListingVolume":null, "onMarketVolume":null }, { "groupByValue":"2017-11", "averageSoldPrice":765272, "medianSoldPrice":null, "maxSoldPrice":15000000, "minSoldPrice":79900, "averageListingPrice":779802, "medianListingPrice":null, "averageDom":23, "medianDom":null, "soldVolume":7239, "newListingVolume":null, "onMarketVolume":null }, { "groupByValue":"2018-02", "averageSoldPrice":776242, "medianSoldPrice":null, "maxSoldPrice":17395000, "minSoldPrice":50000, "averageListingPrice":788079, "medianListingPrice":null, "averageDom":24, "medianDom":null, "soldVolume":5264, "newListingVolume":null, "onMarketVolume":null }, { "groupByValue":"2017-09", "averageSoldPrice":781767, "medianSoldPrice":null, "maxSoldPrice":11307800, "minSoldPrice":41000, "averageListingPrice":797576, "medianListingPrice":null, "averageDom":23, "medianDom":null, "soldVolume":6327, "newListingVolume":null, "onMarketVolume":null }, { "groupByValue":"2017-10", "averageSoldPrice":785460, "medianSoldPrice":null, "maxSoldPrice":9300000, "minSoldPrice":72000, "averageListingPrice":799388, "medianListingPrice":null, "averageDom":22, "medianDom":null, "soldVolume":7069, "newListingVolume":null, "onMarketVolume":null }, { "groupByValue":"2017-06", "averageSoldPrice":798730, "medianSoldPrice":null, "maxSoldPrice":11500000, "minSoldPrice":105000, "averageListingPrice":801603, "medianListingPrice":null, "averageDom":15, "medianDom":null, "soldVolume":7686, "newListingVolume":null, "onMarketVolume":null }, { "groupByValue":"2017-05", "averageSoldPrice":864434, "medianSoldPrice":null, "maxSoldPrice":16000000, "minSoldPrice":2200, "averageListingPrice":831752, "medianListingPrice":null, "averageDom":11, "medianDom":null, "soldVolume":9919, "newListingVolume":null, "onMarketVolume":null }, { "groupByValue":"2017-04", "averageSoldPrice":926513, "medianSoldPrice":null, "maxSoldPrice":9482615, "minSoldPrice":75000, "averageListingPrice":842570, "medianListingPrice":null, "averageDom":9, "medianDom":null, "soldVolume":11477, "newListingVolume":null, "onMarketVolume":null }, { "groupByValue":"2017-03", "averageSoldPrice":927010, "medianSoldPrice":null, "maxSoldPrice":10000000, "minSoldPrice":67000, "averageListingPrice":831688, "medianListingPrice":null, "averageDom":9, "medianDom":null, "soldVolume":11538, "newListingVolume":null, "onMarketVolume":null }, { "groupByValue":"2019-01", "averageSoldPrice":745132, "medianSoldPrice":null, "maxSoldPrice":11250000, "minSoldPrice":110000, "averageListingPrice":761610, "medianListingPrice":null, "averageDom":31, "medianDom":null, "soldVolume":4081, "newListingVolume":null, "onMarketVolume":null }, { "groupByValue":"2018-12", "averageSoldPrice":754575, "medianSoldPrice":null, "maxSoldPrice":5750000, "minSoldPrice":92000, "averageListingPrice":775642, "medianListingPrice":null, "averageDom":31, "medianDom":null, "soldVolume":3704, "newListingVolume":null, "onMarketVolume":null }, { "groupByValue":"2018-08", "averageSoldPrice":760730, "medianSoldPrice":null, "maxSoldPrice":11399000, "minSoldPrice":1900, "averageListingPrice":777780, "medianListingPrice":null, "averageDom":27, "medianDom":null, "soldVolume":6843, "newListingVolume":null, "onMarketVolume":null }, { "groupByValue":"2018-07", "averageSoldPrice":778384, "medianSoldPrice":null, "maxSoldPrice":8040000, "minSoldPrice":80100, "averageListingPrice":793404, "medianListingPrice":null, "averageDom":25, "medianDom":null, "soldVolume":6967, "newListingVolume":null, "onMarketVolume":null }, { "groupByValue":"2018-03", "averageSoldPrice":780230, "medianSoldPrice":null, "maxSoldPrice":7900000, "minSoldPrice":86000, "averageListingPrice":787794, "medianListingPrice":null, "averageDom":19, "medianDom":null, "soldVolume":7538, "newListingVolume":null, "onMarketVolume":null }, { "groupByValue":"2019-02", "averageSoldPrice":783212, "medianSoldPrice":null, "maxSoldPrice":6100000, "minSoldPrice":1100, "averageListingPrice":793552, "medianListingPrice":null, "averageDom":24, "medianDom":null, "soldVolume":5166, "newListingVolume":null, "onMarketVolume":null }, { "groupByValue":"2018-11", "averageSoldPrice":785049, "medianSoldPrice":null, "maxSoldPrice":8415000, "minSoldPrice":100000, "averageListingPrice":799047, "medianListingPrice":null, "averageDom":26, "medianDom":null, "soldVolume":6114, "newListingVolume":null, "onMarketVolume":null }, { "groupByValue":"2018-09", "averageSoldPrice":800085, "medianSoldPrice":null, "maxSoldPrice":8300000, "minSoldPrice":82500, "averageListingPrice":810845, "medianListingPrice":null, "averageDom":25, "medianDom":null, "soldVolume":6768, "newListingVolume":null, "onMarketVolume":null }, { "groupByValue":"2018-10", "averageSoldPrice":805759, "medianSoldPrice":null, "maxSoldPrice":7400000, "minSoldPrice":1450, "averageListingPrice":817011, "medianListingPrice":null, "averageDom":24, "medianDom":null, "soldVolume":7314, "newListingVolume":null, "onMarketVolume":null }, { "groupByValue":"2018-04", "averageSoldPrice":806777, "medianSoldPrice":null, "maxSoldPrice":9500000, "minSoldPrice":55000, "averageListingPrice":812768, "medianListingPrice":null, "averageDom":19, "medianDom":null, "soldVolume":7871, "newListingVolume":null, "onMarketVolume":null }, { "groupByValue":"2018-06", "averageSoldPrice":807386, "medianSoldPrice":null, "maxSoldPrice":12880000, "minSoldPrice":63000, "averageListingPrice":817727, "medianListingPrice":null, "averageDom":21, "medianDom":null, "soldVolume":8143, "newListingVolume":null, "onMarketVolume":null }, { "groupByValue":"2018-05", "averageSoldPrice":807715, "medianSoldPrice":null, "maxSoldPrice":6600000, "minSoldPrice":1700, "averageListingPrice":814303, "medianListingPrice":null, "averageDom":19, "medianDom":null, "soldVolume":8532, "newListingVolume":null, "onMarketVolume":null }]""")
    my_sales.insert_many(sales)
    print('Success')

if __name__=="__main__":
    # 过滤数据
    # data_clean()

    # 主任务
    # get_nearby_and_save()

    # save_estate_to_mongodb()

    # 将区域的边界坐标储存到数据库
    # save_location_to_mongodb()

    # 将地址转化为地理坐标, 并储存到数据库
    # geocoding_save_to_mongodb()

    # 将销售情况, 储存到mongodb
    save_sale_situation_to_mongodb()

    pass