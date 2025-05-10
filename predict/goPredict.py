import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import numpy as np
import tensorflow as tf

#读取数据
data = pd.read_csv('./jobData.csv')

X = data[['city','workExperience','education']]
y = data['maxSalary'].astype(float)

#标签编码
label_encodes = {}
for column in X.columns:
    le = LabelEncoder()
    X[column] = le.fit_transform(X[column])
    label_encodes[column] = le

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=42)

#构建简单的神经网络模型
model = tf.keras.Sequential([
    tf.keras.layers.Dense(64,activation='relu',input_shape=(X_train.shape[1],)),
    tf.keras.layers.Dense(64,activation='relu',),
    tf.keras.layers.Dense(1)
])
model.compile(optimizer='adam',loss='mean_squared_error')

#训练模型
model.fit(X_train,y_train,epochs=5,validation_split=0.2)

def pred_salary(city,workExp,education):
    input_data = pd.DataFrame([[city,workExp,education]],columns=['city','workExperience','education'])

    for column in input_data.columns:
        input_data[column] = label_encodes[column].transform(input_data[column])

    prediction = model.predict(input_data)

    return prediction[0][0]

predicted_salary = pred_salary('成都','经验5-10年','本科')
print(f'预测结果{predicted_salary:.2f}')

