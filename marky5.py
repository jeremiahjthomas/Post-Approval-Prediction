# -*- coding: utf-8 -*-
"""marky5.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1b4EgjY13E12gmgPbGTnl1Kg0YmWyNVrA
"""

from flask import Flask, jsonify, request
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn import preprocessing
from PIL import Image
import urllib.request
import tensorflow as tf
import pandas as pd
import seaborn as sns
import random
import matplotlib.pyplot as plt
from pandas.core.frame import DataFrame

def count_common_keywords(str1, str2, str3):
    words1 = str1.split()
    words2 = str2.split()
    words3 = str3.split()

    set1 = set(words1)
    set2 = set(words2)
    set3 = set(words3)

    common_keywords = set1.intersection(set2)
    common_keywords2 = set2.intersection(set3)
    common_keywords3 = set1.intersection(set3)
    count = len(common_keywords) + len(common_keywords2) + len(common_keywords3)

    return count

data = pd.read_csv("train.csv")
test = pd.read_csv("test.csv")
test_ids = test["id"]
le = preprocessing.LabelEncoder()


#---------------data---------------

data["user_edited"] = le.fit_transform(data["user_edited"])
data["parameters_tone"] = le.fit_transform(data["parameters_tone"])
data["font"] = le.fit_transform(data["font"])
data["parameters_switchboard_template_name"] = le.fit_transform(data["parameters_switchboard_template_name"])

data["parameters_theme"] = le.fit_transform(data["parameters_theme"].str.lower())

data["parameters_prompt_template_name"] = le.fit_transform(data["parameters_prompt_template_name"])
data["has_logo"] = le.fit_transform(data["has_logo"])

data["approved"] = le.fit_transform(data["approved"])

imageList = data["image"]
colorAmtList = []
for image in imageList:
  urllib.request.urlretrieve(image, "curr.png")
  img = Image.open("curr.png")
  img = img.convert("P")
  palette = img.getpalette()
  unique_colors = len(set(palette))
  colorAmtList.append(unique_colors)

data["colorAmt"] = colorAmtList
data.to_csv("train.csv", index=False)
data = data.drop(["image"],axis=1)

set1 = data["caption"]
set2 = data["parameters_chapter_title"]
set3 = data["parameters_chapter_summary"]

commonWordsList = []

for i in range(0,len(data["user_edited"])):
  commonWordsList.append(count_common_keywords(str(set1[i]), str(set2[i]), str(set3[i])))

data["commonWordAmt"] = commonWordsList

data = data.drop(["caption", "parameters_chapter_title", "parameters_chapter_summary", "parameters_photo_search_term"], axis=1)

data = data.drop(['id','user_id','created_at', 'user_created_at'], axis=1)

X = data.drop(['approved'], axis=1)
y = data['approved']

from tensorflow.keras import Sequential
from tensorflow import keras

model = Sequential([
    keras.layers.Dense(200, activation = 'relu', input_shape = (9,)),
    #keras.layers.Dense(200, activation = 'relu'),
    keras.layers.Dense(1, activation = 'sigmoid')

])

opt = keras.optimizers.legacy.Adam(learning_rate = 0.01)
model.compile(loss = 'binary_crossentropy', optimizer=opt, metrics=['accuracy'])

X_train, X_test, y_train, y_test = train_test_split(X,y, test_size = 0.2)

model.fit(X_train, y_train, epochs=50)

model.evaluate(X_test, y_test)

test["user_edited"] = le.fit_transform(test["user_edited"])
test["parameters_tone"] = le.fit_transform(test["parameters_tone"])
test["font"] = le.fit_transform(test["font"])
test["parameters_switchboard_template_name"] = le.fit_transform(test["parameters_switchboard_template_name"])
test["parameters_theme"] = le.fit_transform(test["parameters_theme"].str.lower())
test["parameters_prompt_template_name"] = le.fit_transform(test["parameters_prompt_template_name"])
test["has_logo"] = le.fit_transform(test["has_logo"])

testImageList = test["image"]
testColorAmtList = []
for image in testImageList:
  urllib.request.urlretrieve(image, "curr.png")
  img = Image.open("curr.png")
  img = img.convert("P")
  palette = img.getpalette()
  unique_colors = len(set(palette))
  testColorAmtList.append(unique_colors)

test["colorAmt"] = testColorAmtList
test.to_csv("train.csv", index=False)
test = test.drop(["image"],axis=1)

testSet1 = test["caption"]
testSet2 = test["parameters_chapter_title"]
testSet3 = test["parameters_chapter_summary"]

testCommonWordsList = []

for i in range(0,len(test["user_edited"])):
  testCommonWordsList.append(count_common_keywords(str(testSet1[i]), str(testSet2[i]), str(testSet3[i])))


test["commonWordAmt"] = testCommonWordsList

test = test.drop(["caption", "parameters_chapter_title", "parameters_chapter_summary", "parameters_photo_search_term"], axis=1)
test = test.drop(['id','user_id','created_at', 'user_created_at'], axis=1)

A = test
predictions = model.predict(A)
test

data

import numpy as np
df = pd.DataFrame()
df['id']=test_ids
df['approved']= np.round(predictions,0)


df.to_csv("submission.csv", index=False)

