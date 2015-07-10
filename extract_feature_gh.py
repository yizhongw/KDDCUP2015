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

with open("data/map/categorymap",'r') as f:
    categorymap = pickle.load(f)
with open("data/map/obj_cate",'r') as f:
    obj_cate = pickle.load(f)


with open("data/map/moduletime_map",'r') as f:
    moduletime_map = pickle.load(f)
with open("data/map/modulechild_map",'r') as f:
    modulechild_map = pickle.load(f)    
categorym={}
for i in categorymap:
        #print i,categorymap[i]
        categorym[categorymap[i]]=i
cate_num=len(categorymap)
#print cate_num
user_st = 0
course_st = len(usermap)
obj_st = course_st + len(coursemap)

#print user_st, course_st, obj_st

def find_num_child_parent(visited_module):
        lenn=len(visited_module)
        res=0
        for i in range(0,lenn):
                for j in range(i+1,lenn):
                        #print j,modulechild_map[i]
                        if (j in modulechild_map[i]):
                                res+=1
        return res



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

    st_index = 32
    feature_str = ""
    """
    feature_str += "%d:1" % (userid+st_index,)
    st_index += len(usermap)
    

    feature_str += " %d:1" % (courseid+st_index,)
    st_index += len(coursemap)
    
    feature_str += "".join([" %d:1" % (objid+st_index,) for objid in sorted(objs)])
    st_index += len(objmap)
    """

    
    feature_str += " %d:%d" % (st_index, operation_num)                       # total num of operations
    st_index += 1
    feature_str += " %d:%d" % (st_index, courseid)                        # course_id
    st_index += 1
    
    op_num = [0 for i in range(op_clsnum)]
    server_op_num = [0 for i in range(op_clsnum)]
    browser_op_num = [0 for i in range(op_clsnum)]
    cate=[0 for i in range(cate_num)]
    server_cate=[0 for i in range(cate_num)]
    browser_cate=[0 for i in range(cate_num)]


    sum_diff=[0 for i in range(cate_num)]
    num_diff=[0 for i in range(cate_num)]
    #1,0,0,2014-06-14T09:43:40,server,problem,4
    date_list = []
    date_set = set()
    nowdate=-1
    nowtime=-1
    active_hour=0
    visited_module=[]
    for l in logs:
        #print l
        
        categoryy=int(l[6])
        
        position = l[4]
        #op_id = op_map[l[5]]
        logdate,logtime = l[3].split('T')
        #date_list.append(logdate)
        #print obj_cate[90]
        try:
            tmp=obj_cate[categoryy]
            #print categoryy
            #print obj_cate[categoryy]
        except:
            #print categoryy
            tmp=-1
        if (tmp==-1):
            continue
        if not (categoryy in visited_module):
                visited_module.append(categoryy)
        cate[tmp]+=1
        if(position=="server"):
            server_cate[tmp]+=1
        else:
            browser_cate[tmp]+=1
        
        #cate[categorymap[obj_cate[categoryy]]]+=1
        
        loghour=int(logtime.split(":")[0])
        if (nowdate!=logdate or (nowdate==logdate and nowhour!=loghour)):
            active_hour+=1
            #print logdate,logtime
        #print moduletime_map[categoryy]
        flag=1
        try:
            startdate,starttime=moduletime_map[categoryy].split('T')
        except:
            flag=0
        if (flag==1 and tmp!=-1):
            #print startdate,starttime
            nowtime=logtime
            nowdate=logdate
            nowhour=int(logtime.split(":")[0])
            #print logdate,startdate
            diff_day=(todate(logdate)-todate(startdate)).days
            #print diff_day
            #print diff_day.days
            sum_diff[tmp]+=diff_day
            num_diff[tmp]+=1
    #log_days = len(set(date_list))                    
    #start_date = todate(date_list[0])
    #end_date = todate(date_list[-1])
    #log_datespan = (end_date-start_date).days
    #for i in range(0,14):
        '''
        if (sum_diff[i]==0):
                print 0
        else:
                print float(sum_diff[i]/num_diff[i])
        
        print server_cate[i],browser_cate[i],cate[i]
    '''
    
    
    '''
    for op_id in range(op_clsnum):
        feature_str += " %d:%d" % (op_id+st_index, op_num[op_id])            # num of 7 operations
    st_index += op_clsnum
    
    for op_id in range(op_clsnum):
        feature_str += " %d:%d" % (op_id+st_index, server_op_num[op_id])     # num of 7 operations from server
    st_index += op_clsnum

    for op_id in range(op_clsnum):
        feature_str += " %d:%d" % (op_id+st_index, browser_op_num[op_id])    # num of 7 operations from browser
    st_index += op_clsnum
    '''
    #print visited_module
    #print len(visited_module)

    num_parent=find_num_child_parent(visited_module)
    #print num_parent,len(visited_module)
    #object_category
    for op_id in range(cate_num):
        feature_str += " %d:%d" % (op_id+st_index, cate[op_id])            # num of 7 operations
    st_index += cate_num
    for op_id in range(cate_num):
        feature_str += " %d:%d" % (op_id+st_index, server_cate[op_id])            # num of 7 operations
    st_index += cate_num
    for op_id in range(cate_num):
        feature_str += " %d:%d" % (op_id+st_index, browser_cate[op_id])            # num of 7 operations
    st_index += cate_num
    #print sum_diff
    for op_id in range(cate_num):
        if (sum_diff[op_id]==0):
            feature_str += " %d:%d" % (op_id+st_index, 0)
        else:
            feature_str += " %d:%.3f" % (op_id+st_index, float(float(sum_diff[op_id])/num_diff[op_id]))
            #print sum_diff[op_id]
    st_index += cate_num
    feature_str += " %d:%d" % (st_index, len(visited_module))
    st_index +=1
    feature_str += " %d:%d" % (st_index, num_parent)
    st_index +=1
    if (len(visited_module)==0):
        feature_str += " %d:%.3f" % (st_index, 0)
    else:
        feature_str += " %d:%.3f" % (st_index, float(float(num_parent)/len(visited_module)))
    st_index +=1
    #print feature_str
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
    #print col
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
            #print enrollment_id
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
            #print enrollment_id
            continue
        feature_str = feature_dic[int(enrollment_id)]
        fout.write("0 %s\n" % feature_str)
    fin.close()
    fout.close()    

if __name__=="__main__":
    feature_dic = extract_file("data/clean/log_train.csv",)
    write_train("data/clean/truth_train.csv", feature_dic, "data/feature/train_gh_97")

    feature_dic = extract_file("data/clean/log_test.csv")
    write_test("data/clean/enrollment_test.csv", feature_dic, "data/feature/test_gh_97")
