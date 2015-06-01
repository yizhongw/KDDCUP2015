# enrol_id server{} browser{} all{}
import datetime
op_map = {"nagivate":0, "access":1, "problem":2, "page_close":3, "discussion":4, "video":5, "wiki":6};
op_clsnum = len(op_map);
def todate(s):
    y,m,d = s.split('-');
    return datetime.date(int(y),int(m),int(d));

def todatetime(d,s):
    yy,mm,dd = d.split('-');
    h,m,s = s.split(':');
    return datetime.datetime(int(yy),int(mm),int(dd),int(h),int(m),int(s));

def extract_time(s,active_time):
    #return (todatetime(s,active_time[-1])-todatetime(s,active_time[0])).seconds;
    """
    hr = [line.strip().split(':')[0] for line in active_time];
    return len(set(hr));
    """
    sumoftime = 0;
    upperbound = lowerbound = active_time[0];
    for i in range(len(active_time)):
        if ((i>0) and ((todatetime(s,active_time[i])-todatetime(s,active_time[i-1])).seconds<3600)):
            upperbound = active_time[i];
        elif (i>0):
            sumoftime += (todatetime(s,upperbound)-todatetime(s,lowerbound)).seconds/float(60);
            upperbound = lowerbound = active_time[i];
    sumoftime += (todatetime(s,upperbound)-todatetime(s,lowerbound)).seconds/float(60);
    return sumoftime;


def extract_feature(logcol):
    logs = [line.strip().split(',') for line in logcol];
    operation_num = len(logs);
    feature_str = '';
    st_index = 0;
    op_num = [0 for i in range(op_clsnum)];
    server_op_num = [0 for i in range(op_clsnum)];
    browser_op_num = [0 for i in range(op_clsnum)];
    date_list = [];
    date_set = set();
    active_hour = {};
    active_time = [];
    pre_day = '';
    today = '';
    date_event = {};    #dic: every term is a list with [all,server,browser] for a date
    feature_str += " %d:%d" % (st_index, operation_num)
    st_index += 1
    for l in logs:
        position = l[4];
        op_id = op_map[l[5]];
        op_num[op_id] += 1;
        if (position=='server'):
            server_op_num[op_id] += 1;
        else:
            browser_op_num[op_id] += 1;
        log_date,log_time = l[3].split('T');
        date_list.append(log_date);
        if (log_date==pre_day):
            active_time.append(log_time);
            date_event[log_date][0] += 1;
            if (position=='server'):
                date_event[log_date][1] += 1;
            else:
                date_event[log_date][2] += 1;
        else:
            #timespan.append((totime(active_time[-1])-totime(active_time[0])).hours);
            if (len(active_time)>0):
                delta_time = extract_time(pre_day,active_time);
                active_hour[pre_day] = (delta_time);
            active_time = [log_time,];
            pre_day = log_date;
            if (position=='server'):
                date_event[log_date] = [1,1,0];
            else:
                date_event[log_date] = [1,0,1];
    #timespan.append((active_time[-1]-active_time[0]).hours);      #everyday time span for one user
    delta_time = extract_time(log_date,active_time);
    active_hour[log_date] = (delta_time);
    #all[1..7]+server[1..7]+browser[1..7]
    for op_id in range(op_clsnum):    ##all
        feature_str += ' %d:%d'%(st_index,op_num[op_id])
        st_index += 1;
    for op_id in range(op_clsnum):    ##server
        feature_str += ' %d:%d'%(st_index,server_op_num[op_id])
        st_index += 1;
    for op_id in range(op_clsnum):    ##browser
        feature_str += ' %d:%d'%(st_index,browser_op_num[op_id])
        st_index += 1;
    logdays = len(set(date_list));
    feature_str += ' %d:%d'%(st_index,logdays);     ##active days
    st_index += 1;
    start_date = todate(date_list[0]);
    end_date = todate(date_list[-1]);
    log_datespan = (end_date-start_date).days;
    feature_str += ' %d:%d'%(st_index,log_datespan);    ##Time span
    st_index += 1;
    feature_str += ' %d:%s'%(st_index,logs[-1][3]);      ##Last visit time
    st_index += 1;
    sum = 0;
    for term in active_hour:
        sum += active_hour[term];
    feature_str += ' %d:%f'%(st_index,float(sum)/logdays);        ##average online time
    st_index += 1;
    sum = 0;
    for op_id in range(op_clsnum):    ##sum of all
        sum += op_num[op_id];
    feature_str += ' %d:%f'%(st_index,float(sum)/logdays)
    st_index += 1;
    sum = 0;
    for op_id in range(op_clsnum):    ##sum of server
        sum += server_op_num[op_id];
    feature_str += ' %d:%f'%(st_index,float(sum)/logdays)
    st_index += 1;
    sum = 0;
    for op_id in range(op_clsnum):    ##sum of browser
        sum += browser_op_num[op_id];
    feature_str += ' %d:%f'%(st_index,float(sum)/logdays)
    st_index += 1;
    if (len(date_list)>10):
        K = 10;
    else:
        K = len(date_list);
    latestKDaysEvents = 0;
    latestKDaysHours = 0.0;
    for i in range(K):
        latestKDaysEvents += date_event[date_list[(-1)*i]][0];
        latestKDaysHours += active_hour[date_list[(-1)*i]];
    feature_str += ' %d:%d'%(st_index,latestKDaysEvents)    ##latest K Days Events number
    st_index += 1;
    feature_str += ' %d:%f'%(st_index,latestKDaysHours)     ##latest K Days Active Hours
    st_index += 1;
    deltaEventCube = 0;
    deltaHoursCube = 0.0;
    for i in range(len(date_list)-1):
        day1 = date_list[i];
        day2 = date_list[i+1];
        deltaEventCube += (date_event[day2][0]-date_event[day1][0])**3
        deltaHoursCube += (active_hour[day2]-active_hour[day1])**3
    EventTrend = float(deltaEventCube)/logdays;
    HoursTrend = float(deltaHoursCube)/logdays;
    feature_str += ' %d:%f'%(st_index,EventTrend)     ##Trend of Events
    st_index += 1;
    feature_str += ' %d:%f'%(st_index,HoursTrend)     ##Trend of Active Hours
    st_index += 1;
    return feature_str

def extract_file(logfile):
    fin = open(logfile,'r');
    pre_eid = '';
    col = [];
    feature_dict = {};
    enroll_id = '';
    for line in fin:
        enroll_id = line.split(',')[0];
        if (enroll_id==pre_eid):
            col.append(line);
        else:
            if (len(col)>0):
                feature_str = extract_feature(col);
                feature_dict[int(pre_eid)] = feature_str;
            col = [line,];
            pre_eid = enroll_id;
    feature_str = extract_feature(col);
    feature_dict[int(enroll_id)] = feature_str;
    fin.close();
    return feature_dict;

def write_train(truthfile,feature_dic,outputfile):
    print "Wrinting train file feature....."
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
    print "Wrinting test file feature....."
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
    print "Extracting train file feature...."
    feature_dic = extract_file("../../data/clean/log_train.csv",)
    write_train("../../data/clean/truth_train.csv", feature_dic, "../../data/feature/train_feature2")

    print "Extracting test file feature...."
    feature_dic = extract_file("../../data/clean/log_test.csv")
    write_test("../../data/clean/enrollment_test.csv", feature_dic, "../../data/feature/test_feature2")
