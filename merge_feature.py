import random

fin1 = open("data/feature/train_feature11",'r')


fin2 = open("data/feature/train_gh_97",'r')
fo = open("data/feature/train_gh_97a",'w')

cnt=0
for i in range(0,120542): #80362
    a=fin1.readline()
    b=fin2.readline()
    aa=a.split("\n")[0]
    aa=aa+b[2:]
    fo.write(aa)
    
fin1.close()
fin2.close()
fo.close()

