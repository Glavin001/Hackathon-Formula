import numpy as np
from sklearn.feature_extraction import DictVectorizer


data = np.loadtxt("data.csv",skiprows=1, dtype=object, delimiter=",")

hacks = []
lengtsh = []
for hack in data:
	if len(hack)==8:
		hacks.append(list(hack))

print len(hacks)
data = np.vstack(hacks)
print data.shape

############ PRE PROCESSING BEGINS #########################

# Winner or not
data[:,0] = map(lambda x: x=="True",data[:,0])

# Title of hack
data[:,1] = map(lambda x: len(x),data[:,1])

print data[1]

# Skip tag-line: 2, it contains same info as description and wastes computation

# Description
dv = DictVectorizer()
data[:,2] = map(lambda x: len(x),data[:,2])
data = data[:,:3]

y = data[:,0].ravel()
print "1st",y[0],y.shape
d=0
for n,i in enumerate(y):
	if i:
		d+=1
print "Total",d
x = data[:,1:].astype(float)
# Under-sampling for data imbalencing
x_f = x[y.flatten()==False]
print x_f.shape
y_f = y[y==False]



mask = (y==True)
x = x[mask]
y = y[mask]

#x=np.vstack([x_f[:len(y.flatten())],x])
#y=np.vstack([y_f[:len(y.flatten())],y])

print x.shape
print y.shape

from sklearn.cross_validation import cross_val_score
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import roc_curve, auc
nb = MultinomialNB()

print cross_val_score(nb, x, y, cv=10)
