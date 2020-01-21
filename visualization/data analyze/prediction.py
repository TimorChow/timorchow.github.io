import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from keras.models import Sequential
from keras.layers import LSTM,Dense
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory
#376236 - 822681
from subprocess import check_output

#print(check_output(["input"]).decode("utf8"))

history_data = []
def normalize_data(test_data):
    scl = MinMaxScaler()
    result=scl.fit_transform(test_data)
    return result
#test_data1 = normalize_data(test_data)
test_data= np.loadtxt(open("estate_10years.csv","rb"),delimiter=",",skiprows=0)
test_data = np.reshape(test_data,(120,1))
print(test_data)

#print("cl")
#print(cl[(1+7),0])
def processData(data,lb):
    X,Y = [],[]
    for i in range(len(data)-lb-1):
        X.append(data[i:(i+lb),0])
        print("this  x",X[i])
        Y.append(data[(i+lb),0])
        print("this y",Y[i])
    return np.array(X),np.array(Y)
#X,y = processData(cl,7)
X,y = processData(test_data,3)
#print("raw_length",y.shape)
X_train,X_test = X[:int(X.shape[0]*0.80)],X[int(X.shape[0]*0.80):]
y_train,y_test = y[:int(y.shape[0]*0.80)],y[int(y.shape[0]*0.80):]
print("X_previous",X_test.shape)
#x 是 （1000，7），y是（1000）
print(X_test.shape[0])
print(y_train.shape[0])
print(y_test.shape[0])
model = Sequential()
model.add(LSTM(256,input_shape=(3,1)))
model.add(Dense(1))
model.compile(optimizer='adam',loss='mse')
#Reshape data for (Sample,Timestep,Features)
X_train = X_train.reshape((X_train.shape[0],X_train.shape[1],1))
X_test = X_test.reshape((X_test.shape[0],X_test.shape[1],1))
#Fit model with history to check for overfitting
print("x_train_shape",X_train.shape)
history = model.fit(X_train,y_train,epochs=1000,validation_data=(X_test,y_test),shuffle=False)
#1
#2
Xt = model.predict(X_test)
q1=scl.inverse_transform(y_test.reshape(1,24))
#print("source",q1)
q1_index = [np.linspace(1,24,24)]
q1_index = np.reshape(q1_index,(1,24))
plt.plot(scl.inverse_transform(y_test.reshape(-1,1)))
plt.plot(scl.inverse_transform(Xt))
q2=scl.inverse_transform(Xt)
q2=np.reshape(q2,(1,24))
#print("predict",q2.shape)
q3 = np.concatenate((q1_index,q1), axis=0)
q3=np.stack(q3,axis = 1)


#print("this q3",q3[0])
#print("this q2_index",q2)
plt.show()
#print("this first graph",q3)
#print('this second graph',q2_intact)
#3
act = []
pred = []
#for i in range(250):
i=23
Xt = model.predict(X_test[i].reshape(1,3,1))
print('predicted:{0}, actual:{1}'.format(scl.inverse_transform(Xt),scl.inverse_transform(y_test[i].reshape(-1,1))))
pred.append(scl.inverse_transform(Xt))
act.append(scl.inverse_transform(y_test[i].reshape(-1,1)))
#4
Xt = model.predict(X_test)
plt.plot(scl.inverse_transform(y_test.reshape(-1,1)))
plt.plot(scl.inverse_transform(Xt))
plt.show()
#5
