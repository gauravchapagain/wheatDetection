# importing required libraries

import pandas as pd
import numpy as np
import cv2
import warnings

# saving the model
import pickle

warnings.simplefilter(action='ignore', category=FutureWarning)

# reading csv file and extracting class column to y.
dataf = pd.read_csv("Datasetinfectedhealthy.csv")

# extracting two features
X = dataf.drop(['imgid', 'fold num'], axis=1)
y = X['label']
X = X.drop('label', axis=1)

print("\nTraining dataset:-\n")
print(X)

log = pd.read_csv("E:\Leaf-Disease-Detection-Using-SVM/Datasetunlabelledlog.csv")

log = log.tail(1)
X_ul = log.drop(['imgid', 'fold num'], axis=1)

print("\nTest dataset:-\n")
print(X_ul)

Sum = 0

# Test-train model implementation
from sklearn import metrics
from sklearn.metrics import accuracy_score
from sklearn.metrics import plot_confusion_matrix
from sklearn import svm
from sklearn.model_selection import train_test_split

# test train bujhnalai rakheko
# X_train, Xi_test, y_train, yi_test = model_selection.train_test_split(X, y, train_size=0.25,test_size=0.60)
# print ("X_train: ", X_train)
# print ("y_train: ", y_train)
# print("X_test: ", Xi_test)
# print ("y_test: ", yi_test)
# from sklearn.model_selection import train_test_split

for n in range(4):
    # creating test-train data set
    x_train, Xi_test, y_train, yi_test = train_test_split(X, y, test_size=0.25, random_state=60)

    # create the model
    svclassifier = svm.SVC(kernel='linear')

    # train the model
    svclassifier.fit(x_train, y_train)

    # prediction ko laagi
    pred = svclassifier.predict(X_ul)
    Sum = Sum + pred

# with open('save_data.sav', 'wb') as f:
#     pickle.dump(svclassifier, f)
# with open('save_data.sav', 'rb') as f:
#     sv = pickle.loaded_model(f)
#
# loaded_model = pickle.load(open("save_data.sav", 'rb'))

print("Accuracy: {}%".format(svclassifier.score(Xi_test, yi_test) * 100))

np.set_printoptions(precision=2)

# Plot non-normalized confusion matrix
titles_options = [("Confusion matrix, without normalization", None),
                  ("Normalized confusion matrix", 'true')]
for title, normalize in titles_options:
    disp = plot_confusion_matrix(svclassifier, Xi_test, yi_test)
    disp.ax_.set_title(title)
    print(title)
    print(disp.confusion_matrix)

print("\nprediction: %d" % int(Sum / 4))

if (Sum < 2):
    print("The leaf is sufficiently healthy!")
else:
    print("The leaf is infected!")

print("\nKeypress on any image window to terminate")
cv2.waitKey(0)
