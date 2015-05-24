import pickle
import datetime
with open("data/map/usermap",'r') as f:
	usermap = pickle.load(f)
with open("data/map/coursemap", 'r') as f:
	coursemap = pickle.load(f)
with open("data/map/objectmap", 'r') as f:
	objmap = pickle.load(f)
op_map = {"nagivate":0, "access":1, "problem":2, "page_close":3, "discussion":4, "video":5, "wiki":6}
op_clsnum = len(op_map)

user_st = 0
course_st = len(usermap)
obj_st = course_st + len(coursemap)

print user_st, course_st, obj_st

def todate(s):
	y,m,d = s.split('-')
	return datetime.date(int(y),int(m),int(d))

def extract_feature(logcol):
	logs = [line.strip().split(',') for line in logcol]
	operation_num = len(logs)
	userid = int(logs[0][1])
	courseid = int(logs[0][2])
	objs = set([int(l[6]) for l in logs])
	last_obj = int(logs[-1][6])  # the last operated object
	#print logs[-1]

	st_index = 0

	feature_str = ""
	"""
	feature_str += "%d:1" % (userid+st_index,)
	st_index += len(usermap)
	

	feature_str += " %d:1" % (courseid+st_index,)
	st_index += len(coursemap)
	
	feature_str += "".join([" %d:1" % (objid+st_index,) for objid in sorted(objs)])
	st_index += len(objmap)
	"""
	feature_str += " %d:%d" % (st_index, operation_num)                   	  # total num of operations
	st_index += 1

	op_num = [0 for i in range(op_clsnum)]
	server_op_num = [0 for i in range(op_clsnum)]
	browser_op_num = [0 for i in range(op_clsnum)]
	#1,0,0,2014-06-14T09:43:40,server,problem,4
	date_list = []
	date_set = set()
	for l in logs:
		position = l[4]
		op_id = op_map[l[5]]
		logdate,logtime = l[3].split('T')
		date_list.append(logdate)

		op_num[op_id]+=1
		if(position=="server"):
			server_op_num[op_id]+=1
		else:
			browser_op_num[op_id]+=1

	log_days = len(set(date_list))                    
	start_date = todate(date_list[0])
	end_date = todate(date_list[-1])
	log_datespan = (end_date-start_date).days

	for op_id in range(op_clsnum):
		feature_str += " %d:%d" % (op_id+st_index, op_num[op_id])            # num of 7 operations
	st_index += op_clsnum

	for op_id in range(op_clsnum):
		feature_str += " %d:%d" % (op_id+st_index, server_op_num[op_id])     # num of 7 operations from server
	st_index += op_clsnum

	for op_id in range(op_clsnum):
		feature_str += " %d:%d" % (op_id+st_index, browser_op_num[op_id])    # num of 7 operations from browser
	st_index += op_clsnum

	feature_str + " %d:%d" % (st_index, log_days)                            # active days
	st_index += 1

	feature_str += " %d:%d" % (st_index, log_datespan)                       # active time span
	st_index += 1

	return feature_str

def extract_file(logfile):
	fin = open(logfile,'r')	

	prev_eid = ""
	col = []
	feature_dic = {}
	enroll_id = ""
	for line in fin:
		enroll_id = line.split(',',1)[0]
		if enroll_id == prev_eid:
			col.append(line)			
		else:
			if(len(col)>0):
				feature_str = extract_feature(col)
				feature_dic[int(prev_eid)] = feature_str
			col = [line,]
			prev_eid = enroll_id
	#process log of the last enrollment id
	feature_str = extract_feature(col)
	feature_dic[int(enroll_id)] = feature_str
	fin.close()
	
	return feature_dic

def write_train(truthfile,feature_dic,outputfile):
	fin = open(truthfile)
	fout = open(outputfile,'w')
	
	for line in fin:
		enrollment_id, label = line.strip().split(',')
		if int(enrollment_id) not in feature_dic:
			print enrollment_id
			continue
		feature_str = feature_dic[int(enrollment_id)]
		fout.write("%s %s\n" % (label, feature_str))
	fin.close()
	fout.close()

def write_test(testfile, feature_dic, outputfile):
	fin = open(testfile)
	fout = open(outputfile,'w')
	for line in fin:
		enrollment_id, remain = line.strip().split(',',1)
		if int(enrollment_id) not in feature_dic:
			print enrollment_id
			continue
		feature_str = feature_dic[int(enrollment_id)]
		fout.write("0 %s\n" % feature_str)
	fin.close()
	fout.close()	

if __name__=="__main__":
	feature_dic = extract_file("data/clean/log_train.csv",)
	write_train("data/clean/truth_train.csv", feature_dic, "data/feature/train")

	feature_dic = extract_file("data/clean/log_test.csv")
	write_test("data/clean/enrollment_test.csv", feature_dic, "data/feature/test")