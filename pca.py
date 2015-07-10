import numpy as np
from sklearn.decomposition import PCA
from sklearn.decomposition import SparsePCA

n_feat=97


fin = open("data/feature/train_gh_97a",'r')

fo=open("data/feature/train_gh_97a_PCA",'w')
cnt=0
feature=[[0 for i in range(0,n_feat)] for j in range(0,120542)] #80362
for line in fin:
    a=line.split(" ")
    for i in range(2,n_feat):
        feature[cnt][i-2]=float(a[i].split(":")[1])
    cnt+=1
print cnt
#print feature[cnt-1]

X=np.array(feature)
'''
pca=PCA(n_components=n_feat)
pca_result=pca.fit_transform(X)
'''
pca=SparsePCA(n_components=n_feat,alpha=0.6,n_jobs=2,max_iter=15)
pca_result=pca.fit_transform(X)

#print pca_result[0]
cnt=0
fin = open("data/feature/train_gh_97a",'r')

for line in fin:
    a=line.split(" ")
    PCA_d=50
    for i in range(0,PCA_d):
        a[i+2]=str(i)+":"+str(feature[cnt][i])
    ll=" ".join(a[0:PCA_d+2])
    fo.write(ll+"\n")
    cnt+=1
fo.close()