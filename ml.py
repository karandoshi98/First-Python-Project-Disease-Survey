import Create_csv as cc
import pandas as pd
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LogisticRegression

class ML:
    def __init__(self):
        pass

    def preprocess(self, a, y, t):
        cc.Create_csv()
        df1 = pd.read_csv('/home/karan/PycharmProjects/coll_proj/data.csv')
        df1.loc[df1["d_type"] == 'Deadly', 'class'] = 0
        df1.loc[df1["d_type"] == 'Not deadly', 'class'] = 1

        df1.drop(columns=['name', 'd_type'], inplace=True)

        df1.loc[df1["disease"] == 'Stroke', 'dis'] = 2
        df1.loc[df1["disease"] == 'Cancer', 'dis'] = 3
        df1.loc[df1["disease"] == 'Heart Disease', 'dis'] = 4
        df1.loc[df1["disease"] == 'Malaria', 'dis'] = 5
        df1.loc[df1["disease"] == 'Diabetes', 'dis'] = 6
        df1.loc[df1["disease"] == 'Tumor', 'dis'] = 7
        df1.loc[df1["disease"] == 'Asthma', 'dis'] = 8
        df1.loc[df1["disease"] == 'Diarrhea', 'dis'] = 9
        df1.loc[df1["disease"] == 'Depression', 'dis'] = 10
        df1.loc[df1["disease"] == 'Flu', 'dis'] = 11

        df1_dis = df1['disease']
        df1.drop(columns='disease', inplace=True)

        X = np.array(df1.drop(['class'], 1))
        Y = np.array(df1['class'])

        ob = ML()

        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2)

        clf, X_train1, X_test1, y_train1, y_test1, accuracy=ob.train(X_train, X_test, y_train, y_test)
        clf1, X_train, X_test, y_train, y_test, accuracy=ob.train(X_train1, X_test1, y_train1, y_test1)

        # a=age
        # y=year
        # t=type

        pred = ob.predict1(clf1,a,y,t)
        return pred,accuracy


    def train(self,X_train, X_test, y_train, y_test):
        clf = LogisticRegression()
        clf.fit(X_train, y_train)
        accuracy = clf.score(X_test, y_test)
        # print(accuracy)
        return clf,X_train, X_test, y_train, y_test, accuracy

    def predict1(self,clf,a,y,t):
        test_measures = np.array([[a, y, t]])
        prediction = clf.predict(test_measures)

        # print(prediction)
        return prediction