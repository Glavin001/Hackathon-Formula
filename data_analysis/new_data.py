import cPickle as pickle
import numpy as np
data = None
with open("raw_data.p", 'rb') as fp:
  data = pickle.load(fp)
data = np.vstack(data)
print data.shape
