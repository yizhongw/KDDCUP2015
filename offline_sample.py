import random
fin = open("data/feature/train_gh_52_20",'r')
fo1 = open("data/feature/train_gh_52_20_1",'w')
fo2 = open("data/feature/train_gh_52_20_2",'w')

for line in fin:
	if random.uniform(0,1)<0.75:
		fo1.write(line)
	else:
		fo2.write(line)
fin.close()
fo1.close()
fo2.close()