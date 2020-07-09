import numpy as np
import matplotlib
import matplotlib.pyplot as plt



def cont_frac_exp(x, steps):
    exp = np.empty([np.size(x), steps], dtype = int)
    part = 1./x
    for i in xrange(steps):
        exp[:,i] = np.floor(part)
        part -= exp[:,i]
        part[part != 0] = 1./part[part != 0]
    exp[exp <= 0] = 0
    return exp

def questmark(frac):
    outlen = np.shape(frac)[0]
    explen = np.shape(frac)[1]
    out = np.zeros(outlen)
    for i in xrange(outlen):
        if np.all(frac[i,np.arange(1, explen, 2)] == 0) and np.any(frac[i,:] != 0):
            ind = np.where(frac[i,:] != 0)[0][0]
            frac[i, ind] -= 1
            frac[i, ind + 1] += 1
    for i in xrange(explen-1):
        frac[:,i+1] += frac[:,i]
        if i % 2 == 0:
            for j in xrange(outlen):
                out[j] += sum(2.**np.arange(1-frac[j,i+1],1-frac[j,i]))
    return out

def preim(x):
    return np.append(1./(x+1.), x/(x+1.))

def collectpreim(x, n):
    temp = np.array([x])
    coll = temp
    for i in xrange(n):
        temp = preim(temp)
        coll = np.append(coll, temp)
    return coll

def g(a, arr):
    return float(np.size(arr[arr < a])) / arr.size

datapts = 1000
X = np.linspace(0, 1, datapts)
Y2 = questmark(cont_frac_exp(X, 50))
Y1 = np.arange(datapts, dtype = float)
arr1 = collectpreim(1/np.sqrt(2), 20)
for i in xrange(datapts):
    Y1[i] = g(X[i], arr1)
plt.subplot2grid((5,1), (0,0), rowspan=4, colspan=1)
plt.plot(X, Y1)
plt.plot(X, Y2)
plt.subplot2grid((5,1), (4,0), rowspan=1, colspan=1)
diff = np.zeros(datapts)
d = Y1-Y2
plt.plot(X, d)
plt.show()
