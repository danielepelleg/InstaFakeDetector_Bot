import pandas as pd
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from scraper import scrapeAccount


df = pd.read_csv("./resources/DataSet.csv")
X = df.iloc[:, 0:11].values
y = df[['Fake']]

"""
    Set the Train set and the Test set
"""
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

"""
    Set the Decision Tree Classifier algorithm
"""
#AdaBoost
from sklearn.ensemble import AdaBoostClassifier
clf = AdaBoostClassifier(n_estimators=100, random_state=0)
# train the algorithm
clf.fit(X_train, y_train.values.ravel())

"""
    Get the result array and transform it to a String.
    0 -> Real Account
    1 -> Fake Account
"""
def getPrediction(result):
  number = result[0][0]
  switcher = {
      0: "real",
      1: "fake"
  }
  return switcher.get(number, "invalid")

"""
    Get the probability the result is a success 
    Percentage value.
"""
def getProbability(result):
    prediction = result[0][0]
    if (prediction == 0):
        probability = result[1][0][0]
    else: probability = result[1][0][1]

    return'{:.1%}'.format(probability)


def predict(username):
    result = []
    account = scrapeAccount(username)
    prediction = clf.predict(account)
    probability = clf.predict_proba(account)
    result.append(prediction)
    result.append(probability)
    print(result)

    return result
    

