import pandas as pd
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from scraper import scrapeAccount

"""
    Train the Ada Boost algorithm with a dataset or another
        whether an account is private or not 
"""
def trainAlgorithm(dictionaryLen):
    if (dictionaryLen == 11):
        df = pd.read_csv("./resources/DefaultDataSet.csv")
        X = df.iloc[:, 0:11].values

    elif (dictionaryLen == 14):
        df = pd.read_csv("./resources/OpenDataSet.csv")
        X = df.iloc[:, 0:14].values
    
    y = df[['Fake']]

    """
        Set the Train set and the Test set
    """
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

    """
        Set the AdaBoost Classifier algorithm
    """
    #AdaBoost
    from sklearn.ensemble import AdaBoostClassifier
    clf = AdaBoostClassifier(n_estimators=100, random_state=0)
    # train the algorithm
    clf.fit(X_train, y_train.values.ravel())
    return clf

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
    Get the probability of the result
    Percentage value.
"""
def getProbability(result):
    # Take the result 0 or 1
    prediction = result[0][0]
    # If the User has been classified as real
    if (prediction == 0):
        # Takes the percentage for real account
        probability = result[1][0][0]
    # Else takes the percentage for fake account
    else: probability = result[1][0][1]

    # Forma to percentage
    return'{:.1%}'.format(probability)

"""
    Predict the authenticity of the account
"""
def predict(username):
    result = []
    account = scrapeAccount(username)
    if (account != None):
        clf = trainAlgorithm(len(account[0]))
        prediction = clf.predict(account)
        probability = clf.predict_proba(account)
        result.append(prediction)
        result.append(probability)
        print(result)

        return result
        
    else: return None
    

