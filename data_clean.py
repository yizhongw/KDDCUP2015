import pickle

course_map = {}
user_map = {}
obj_map = {}
enrollment_user_course = {}

def retrive(key, dic):
	if key in dic:
		res = dic[key]
	else:
		res = len(dic)
		dic[key] = res
	return res

def clean_enrollment(fn):
	print fn
	fin = open("data/raw/"+fn,'r')
	fout = open("data/clean/"+fn,'w')

	fin.readline()
	for row in fin:
		arg = row.strip().split(',')
		user_index = retrive(arg[1], user_map)
		course_index = retrive(arg[2], course_map)
		fout.write("%s,%d,%d\n" % (arg[0], user_index, course_index))
		# enrollment id with its corresponding user index and course index
		enrollment_user_course[arg[0]] = (user_index,course_index) 
	fin.close()
	fout.close()

def clean_log(fn):
	print fn
	fin = open("data/raw/"+fn,'r')
	fout = open("data/clean/"+fn,'w')

	fin.readline()
	for row in fin:
		arg = row.strip().split(',')
		#enrollment_id,username,course_id,time,source,event,object
		fout.write("%s,%d,%d,%s,%s,%s,%d\n" % (arg[0], enrollment_user_course[arg[0]][0],
			enrollment_user_course[arg[0]][1], arg[1], arg[2], arg[3], retrive(arg[4], obj_map)))
	fin.close()
	fout.close()

def clean_object(fn):
	print fn
	fin = open("data/raw/"+fn,'r')
	fout = open("data/clean/"+fn,'w')

	fin.readline()
	for row in fin:
		arg = row.strip().split(',')
		#course_id,module_id,category,
		fout.write("%d,%d,%s," % (retrive(arg[0],course_map),retrive(arg[1],obj_map),arg[2]))
		#children
		children = arg[3].split(' ')
		for child_object in children:
			if child_object:
				fout.write("%d " % retrive(child_object,obj_map))
		#start
		fout.write(",%s\n" % arg[4])


if __name__ == "__main__":
	clean_enrollment("enrollment_train.csv")
	clean_log("log_train.csv")
	clean_enrollment("enrollment_test.csv")
	clean_log("log_test.csv")
	clean_object("object.csv")
	with open("data/map/usermap",'w') as f:
		pickle.dump(user_map, f)
	with open("data/map/coursemap", 'w') as f:
		pickle.dump(course_map, f)
	with open("data/map/objectmap", 'w') as f:
		pickle.dump(obj_map, f)
