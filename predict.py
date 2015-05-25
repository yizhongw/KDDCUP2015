from sklearn.datasets import *
from sklearn.ensemble import *
from sklearn.metrics import roc_curve
from sklearn.metrics import auc 
import numpy

X_train, y_train, X_test, y_test = load_svmlight_files(("data/feature/train_1","data/feature/train_2"))

y_test = numpy.array(y_test)

''' # Ramdom Forest
rf_classifier = RandomForestClassifier(n_estimators = 100, max_depth = None, min_samples_split = 1, random_state = 0, max_features = 5, verbose = 1, n_jobs = -1)
#classifier = RandomForestClassifier(n_estimators = 50, min_samples_leaf=10, verbose=1)
rf_classifier.fit(X_train, y_train)
y_prob = rf_classifier.predict_proba(X_test)
'''

# Gradient Boosting
gbrt_classifier = GradientBoostingClassifier(n_estimators=100, max_depth=3)
gbrt_classifier.fit(X_train.toarray(),y_train)
y_prob = gbrt_classifier.predict_proba(X_test.toarray())

y_pred = y_prob[:,1]

'''
sample_submission_file = open('data/raw/sampleSubmission.csv')
submission_file = open('data/submission/submission_yz_20150525.csv','w')
cnt = 0
for line in sample_submission_file:
	enroll_id = line.split(',')[0]
	new_line = enroll_id + ',' + str(y_pred[cnt]) + '\n'
	submission_file.write(new_line)
	cnt += 1
print cnt
sample_submission_file.close()
submission_file.close()

'''

print "SHAPE"
print len(y_pred)

fpr, tpr, thresholds = roc_curve(y_test, y_pred, pos_label=1)  
print auc(fpr, tpr)


#print thresholds

#print rf_classifier.score(X_test, y_test)

