import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from copy import deepcopy
from string import ascii_letters
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib import colors as mcolors

# calculate possible Rauzy-Veech induction pre-image for a pair of interval lengths and label order
def preim(perm, lens):
    dim = len(lens)
    ind = np.where(perm[0,:] == perm[1,dim-1])[0][0]
    lens1 = deepcopy(lens)
    lens1[perm[0,ind]] += lens1[perm[0,ind+1]]
    p0 = np.concatenate((perm[0,:ind+1], perm[0,ind+2:], [perm[0,ind+1]]))
    p1 = np.concatenate(([p0], [perm[1,:]]), axis=0)
    ind = np.where(perm[1,:] == perm[0,dim-1])[0][0]
    p0 = np.concatenate((perm[1,:ind+1], perm[1,ind+2:], [perm[1,ind+1]]))
    p2 = np.concatenate(([perm[0,:]], [p0]), axis=0)
    lens2 = deepcopy(lens)
    lens2[perm[1,ind]] += lens1[perm[1,ind+1]]
    permout = [p1, p2]
    lensout = [lens1/np.sum(lens1), lens2/np.sum(lens2)]
    return permout, lensout

# reduces permutations from the form [[0, 1, 2, 3], [3, 2, 1, 0]] to ['d','c','b','a'] in the list of permutations perms so that a permutation is uniquely defined
def permcheck(perms):
    num = len(perms)
    simpleperms = range(num)
    for j in range(num):
        perm = perms[j]
        dim = np.shape(perm)[1]
        simpleperm = range(dim)
        for i in range(dim):
            simpleperm[np.where(perm[1,:] == perm[0,i])[0][0]] = ascii_letters[i]
        simpleperms[j] = simpleperm
    return simpleperms

perm = np.array([[0, 1, 2, 3], [3, 2, 1, 0]]) # initial permutation
lens = np.array([0.2, 0.3, 0.1, 0.4]) # initial interval lengths
complete = permcheck(np.array([perm]))
end = complete[0]
points = [lens]
newperms = [perm]
newlens = [lens]
flag = True

# generates the list of all possible Rauzy-Veech pre-images given an initial permutation and interval lengths, collecting all such generated points
while flag or (newperms != []):
    newnewperms = []
    newnewlens = []
    for i in xrange(len(newperms)):
        newp, newl = preim(newperms[i], newlens[i])
        points += newl
        simplenew = permcheck(newp)
        if end in simplenew:
            flag = False
        ind = np.array([simplenew[0] not in complete, simplenew[1] not in complete])
        newnewperms += list(np.array(newp)[ind])
        newnewlens += list(np.array(newl)[ind])
        complete += (np.array(simplenew)[ind]).tolist() # do not move!
    newperms = deepcopy(newnewperms)
    newlens = deepcopy(newnewlens)

points = np.array(points)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(points[:,0], points[:,1], points[:,2])
x = [1,0,0]
y = [0,1,0]
z = [0,0,1]
verts = [zip(x,y,z)]
ax.add_collection3d(Poly3DCollection(verts, facecolors = mcolors.to_rgba('y', alpha=0.1)))
ax.scatter(1,1,1)
plt.show()
