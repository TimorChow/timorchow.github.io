import pymongo
import numpy as np
import json
from gmplot import gmplot

GOOGLE_API_KEY = 'AIzaSyA0DCbrEFr-QWhbY6edjz9lGYY_smPuICM' # timorchow1@gmail.com
AWS = '18.221.97.18'
Local = 'localhost'


myclient = pymongo.MongoClient("mongodb://{}:27017/".format(AWS))
mydb = myclient['51ca']
my_estate = mydb["estate"]
my_boundary = mydb['boundary']
my_assault = mydb['assault']

# Place map
center_lat = 43.725811
center_lng = -79.390297
gmap = gmplot.GoogleMapPlotter(center_lat, center_lng, 11, apikey=GOOGLE_API_KEY)

def draw_boundary():
    '''
    draw boundary of a area on google map
    :return:
    '''

    # Polygon 多边形
    # city_names_list = ['toronto', 'markhanm', 'mississauga', 'oakville', 'richmondhill', 'vaughan']
    city_names_list = ['toronto']
    for city_name in city_names_list:
        boundary_list = get_boundary(city_name)
        lats, lons = zip(*boundary_list)
        print(lats)
        gmap.plot(lats, lons, 'cornflowerblue', edge_width=10)

    # Scatter points
    # boundary_list = get_boundary(city_name)
    # top_attraction_lats, top_attraction_lons = zip(*boundary_list)
    # gmap.scatter(top_attraction_lats, top_attraction_lons, '#3B0B39', size=40, marker=False)

    # Marker
    hidden_gem_lat, hidden_gem_lon = 37.770776, -122.461689
    gmap.marker(hidden_gem_lat, hidden_gem_lon, 'cornflowerblue')

    # Draw
    gmap.draw("my_map.html")

def get_boundary(city_name):
    boundary_list = my_boundary.find_one({'city_name': city_name})['boundary']
    result = [(boundary['lat'], boundary['lng']) for boundary in boundary_list]
    return result


def draw_assault_heatmap():
    """
    画犯罪率地图关键参数: 高斯分布方差, 犯罪率normalize
    :return:
    """
    assault_list_mongodb = my_assault.find()
    assault_list = [assault for assault in assault_list_mongodb]
    # 将犯罪频率降低降低(否则密密麻麻看不清)
    result_list = [[assault['lat'], assault['lng'], int(assault['2018'])//5] for assault in assault_list]
    result_list_np = np.array(result_list)

    repeated_list = np.array([[center_lat, center_lng]])
    for assault in result_list_np:
        # 获得当前区域中心点和犯罪数量
        lat, lng, count = assault[0], assault[1], int(assault[2])
        # 根据中心点随机生成n个点, n为犯罪数量
        rand_point = np.random.normal([lat, lng], 0.01, [count, 2])

        # 合并已知的点
        rand_point = np.append(rand_point,[[lat, lng]], axis=0)
        repeated_list = np.append(rand_point, repeated_list, axis=0)

    # 转置数组, 取出其lat和lng
    repeated_np_list = np.transpose(np.array(repeated_list))
    latitude_list = repeated_np_list[0]
    longitude_list = repeated_np_list[1]

    # print(latitude_list)
    gmap.heatmap(latitude_list, longitude_list)


    gmap.circle(43.73830244, -79.29570204, 500, "#0000FF", ew=2)
    gmap.circle(43.68903698, -79.46478937, 500, "#0000FF", ew=2)


    # # Write the map in an HTML file
    gmap.draw('assault_heatmap.html')


def draw_price_heatmap():
    """
    Draw a price heatmap
    :return:
    """
    total_latitude_list = np.array([center_lat])
    total_longitude_list = np.array([center_lng])

    for i in range(10):
        estate_list_mongodb = my_estate.find().limit(200).skip(200*i)
        estate_list = [estate for estate in estate_list_mongodb]
        # normalized
        multiple = 500000
        result_list = [[estate['latitude'], estate['longitude'], int(float(estate['price']))//multiple] for estate in estate_list]
        result_list_np = np.array(result_list)

        repeated_list = np.array([[43.725811, -79.390297]])
        for estate in result_list_np:
            # get the coordinate and price index
            lat, lng, count = float(estate[0]), float(estate[1]), int(estate[2])
            # according to the price index, make normal distribution point
            rand_point = np.random.normal([lat, lng], 0.008, [count, 2])

            rand_point = np.append(rand_point,[[lat, lng]], axis=0)
            repeated_list = np.append(rand_point, repeated_list, axis=0)

        # transpose [n, 2] to [2, n]
        repeated_np_list = np.transpose(np.array(repeated_list))
        latitude_list = repeated_np_list[0]
        longitude_list = repeated_np_list[1]

        total_latitude_list = np.append(total_latitude_list, latitude_list)
        total_longitude_list = np.append(total_longitude_list, longitude_list)

        print('Success: ', total_latitude_list.shape[0])

    gmap.heatmap(total_latitude_list, total_longitude_list)


    gmap.circle(43.76484034, -79.36864246, 500, "#0000FF", ew=2)
    gmap.circle(43.77163083, -79.57974515, 500, "#0000FF", ew=2)


    # # Write the map in an HTML file
    gmap.draw('price_heatmap.html')


def gmplot_demo():
    mymap = gmplot.GoogleMapPlotter(37.428, -122.145, 16, apikey=GOOGLE_API_KEY)
    # mymap = GoogleMapPlotter.from_geocode("Stanford University")

    # mymap.grid(37.42, 37.43, 0.001, -122.15, -122.14, 0.001)
    # mymap.marker(37.427, -122.145, "yellow")
    # mymap.marker(37.428, -122.146, "cornflowerblue")
    # mymap.marker(37.429, -122.144, "k")

    lat, lng = mymap.geocode("Stanford University")
    mymap.marker(lat, lng, "red")


    mymap.circle(37.429, -122.145, 100, "#FF0000", ew=2)
    path = [(37.429, 37.428, 37.427, 37.427, 37.427),
             (-122.145, -122.145, -122.145, -122.146, -122.146)]
    path2 = [[i+.01 for i in path[0]], [i+.02 for i in path[1]]]
    path3 = [(37.433302 , 37.431257 , 37.427644 , 37.430303), (-122.14488, -122.133121, -122.137799, -122.148743)]
    path4 = [(37.423074, 37.422700, 37.422410, 37.422188, 37.422274, 37.422495, 37.422962, 37.423552, 37.424387, 37.425920, 37.425937),
         (-122.150288, -122.149794, -122.148936, -122.148142, -122.146747, -122.14561, -122.144773, -122.143936, -122.142992, -122.147863, -122.145953)]
    # mymap.plot(path[0], path[1], "plum", edge_width=10)
    # mymap.plot(path2[0], path2[1], "red")
    # 多边形
    # mymap.polygon(path3[0], path3[1], edge_color="cyan", edge_width=5, face_color="blue", face_alpha=0.1)

    # mymap.heatmap(path4[0], path4[1], threshold=10, radius=40)
    print(path4[0])
    # mymap.heatmap(path3[0], path3[1], threshold=10, radius=40, dissipating=False, gradient=[(30,30,30,0), (30,30,30,1), (50, 50, 50, 1)])
    # mymap.scatter(path4[0], path4[1], c='r', marker=True)
    # mymap.scatter(path4[0], path4[1], s=90, marker=False, alpha=0.1)
    # Get more points with:
    # http://www.findlatitudeandlongitude.com/click-lat-lng-list/
    scatter_path = ([37.424435, 37.424417, 37.424417, 37.424554, 37.424775, 37.425099, 37.425235, 37.425082, 37.424656, 37.423957, 37.422952, 37.421759, 37.420447, 37.419135, 37.417822, 37.417209],
                    [-122.142048, -122.141275, -122.140503, -122.139688, -122.138872, -122.138078, -122.137241, -122.136405, -122.135568, -122.134731, -122.133894, -122.133057, -122.13222, -122.131383, -122.130557, -122.129999])
    mymap.scatter(scatter_path[0], scatter_path[1], c='r', marker=True)
    mymap.draw('./mymap_demo.html')


if __name__ == "__main__":
    # draw_boundary()
    # get_boundary()
    # draw_assault_heatmap()
    draw_price_heatmap()
    # gmplot_demo()
    # print(float('2298000.00')//2)
