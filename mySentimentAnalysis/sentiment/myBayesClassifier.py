'''
Created on 15. ozu 2018.

@author: Katarina123
'''

from sklearn.naive_bayes import GaussianNB
import numpy as np


x = np.array([1, 2, 10, 9, 11, 13, 28, 29, 30]).reshape(-1, 1)
y = np.array([1, 0, 0, 1, 0, 1, 0, 0, 0])

#Create a Gaussian Classifier
model = GaussianNB()

# Train the model using the training sets 
model.fit(x, y)

#Predict Output 
predicted= model.predict([[2,1],[21,1]])
print (predicted)