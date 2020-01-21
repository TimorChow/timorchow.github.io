import matplotlib.pyplot as plt
import mplleaflet
import numpy as np
from skimage import draw,data
# x = y = np.arange(-4, 4, 0.1)
# x, y = np.meshgrid(x,y)
# plt.contour(x, y, x**2 + y**2, [9])     #x**2 + y**2 = 9 的圆形
#
# plt.axis('scaled')
def draw_circle():
    r=0.3
    a, b = (121.31, 31.13)
    # ==========================================
    # 方法一：参数方程
    theta = np.arange(0, 2*np.pi, 0.01)
    x = a +  np.cos(theta)
    y = b +  np.sin(theta)
    print('circle')
    print(np.cos(theta))
    plt.plot(x,y,color = 'yellow',linewidth ='1')
    #内圆
    x_in = np.cos(theta)
    y_in = np.sin(theta)
    plt.plot(x_in,y_in,color = 'blue',linewidth = '1')
    #plt.plot(x,y,'zzz')
    #fig = plt.figure()
    #axes = fig.add_subplot(111)
    #theta = np.linspace(0, 2 * np.pi, 500)
    v = np.linspace(1.01,1.99,10)
    v.shape = (10, 1)
    x1 = v*(a+np.cos(theta))
    y1 = v*(b+np.sin(theta))
    print("full")
    print(x1[0])
    print("full_y")
    print(y[0])
    #y1 = v * y
    plt.plot(x1, y1, color='yellow', linewidth=2.0)
    plt.show()
    #axes.plot(x, y)

    v = np.linspace(1.01,1.99,10)
    print(v)
    print(x)
    v.shape = (10,1)
    x1 = v*x
    print(x1.shape)
    y1 = v*y
    plt.plot(x1,y1,color = 'yellow',linewidth = 1)
    # fig1 = plt.figure()
    # axes1 = fig1.add_subplot(222)
    # axes1.plot(x1,y1)
    # fig.canvas.draw()
    #axes.axis('equal')
    plt.title('www.jb51.net')

#draw_circle()
def stupid_circle():
    long = -79.43902830
    lat = 43.721919000
    coordinat = np.array([long,lat])
    print(coordinat.shape)
    new_centroid = np.tile(coordinat,(629,1))
    #new_centroid=new_centroid.reshape(2,629)
    print(new_centroid)
    print(new_centroid.shape)
    theta = np.arange(0, 2 * np.pi, 0.01)
    x = long + np.cos(theta)
    y = lat + np.sin(theta)
    out_circle = np.array([x,y])
    out_circle=out_circle.reshape(629,2)
    print(out_circle.shape)
    plt.plot(out_circle,new_centroid,color ='yellow')
#stupid_circle()
#外圆
theta =np.arange(0, 2*np.pi, 0.01)
x,y = np.cos(theta)-79.43902830, np.sin(theta)+43.721919000
#plt.plot(x, y, 'bd')
#内圆
num_fill = np.linspace(0,0.007,100)
for i in range(len(num_fill)):
    x,y = np.cos(theta)*num_fill[i]-79.43902830,np.sin(theta)*num_fill[i]+43.721919000
    plt.plot(x,y,'r-',color = "blue",linewidth=10.0,alpha = 0.05)

#x1,y1 = 2+np.cos(theta), 2+np.sin(theta)
#plt.plot(x1, y1, color='yellow', linewidth=2.0)
#v = np.linspace(2,2,20)
#print(v.shape)
#print(v)

#v.shape = (20, 1)

#x1 = v * (x1)
#print("x1shape",x1.shape)
#y1 = v * (y1)
#plt.plot(x1, y1, color='yellow', linewidth=2.0)
#plt.show()
#rr,cc = draw.circle(150,150,50)
#draw.set_color(img,[rr,cc],[0,255,0])
plt.plot(-79.43902830, 43.721919000, 'gs') # fast repair
mplleaflet.show(tiles='cartodb_positron', path='pot_holes.html')

