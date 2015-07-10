from sklearn.datasets import *
from sklearn.ensemble import *
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn import linear_model
from sklearn.metrics import roc_curve
from sklearn.metrics import auc 
from sklearn.tree import DecisionTreeClassifier
from datetime import date
import numpy

def offline_score(y_test, y_pred):
	fpr, tpr, thresholds = roc_curve(y_test, y_pred, pos_label=1)  
	return auc(fpr, tpr)

def write_file(y_pred, outfilename):
	sample_submission_file = open('data/raw/sampleSubmission.csv')
	today = date.today().isoformat()
	submission_file = open('data/submission/' + outfilename + '_' + today + '.csv','w')
	cnt = 0
	for line in sample_submission_file:
		enroll_id = line.split(',')[0]
		new_line = enroll_id + ',' + str(y_pred[cnt]) + '\n'
		submission_file.write(new_line)
		cnt += 1
	sample_submission_file.close()
	submission_file.close()

def knn(X_train, y_train, X_test):
	knn_classifier = KNeighborsClassifier(n_neighbors=3)
	knn_classifier.fit(X_train, y_train)
	y_prob = knn_classifier.predict_proba(X_test)
	y_pred = y_prob[:,1]
	return y_pred


def logistic_regression(X_train, y_train, X_test):
	lr_classifier = linear_model.LogisticRegression(penalty='l2', 
		dual=False, tol=0.0001, C=1.0, fit_intercept=True, 
		intercept_scaling=1, class_weight=None, random_state=None, 
		solver='liblinear', max_iter=1000, multi_class='ovr', verbose=1)
	lr_classifier.fit(X_train, y_train)
	y_prob = lr_classifier.predict_proba(X_test)
	y_pred = y_prob[:,1]
	return y_pred

def svm(X_train, y_train, X_test):
	svm_classifier = SVC(kernel="linear", C=0.025, verbose=1) # LinearSVC()
	svm_classifier.fit(X_train, y_train)
	y_prob = svm_classifier.predict_proba(X_test)
	y_pred = y_prob[:,1]
	return y_pred

def neural_network():
	pass

def ada_boost(X_train, y_train, X_test):
	ada_classifier = AdaBoostClassifier(base_estimator = RandomForestClassifier(),
										n_estimators = 5)
	ada_classifier.fit(X_train,y_train)
	y_prob = ada_classifier.predict_proba(X_test)
	y_pred = y_prob[:,1]
	return y_pred

def random_forest(X_train, y_train, X_test):
	rf_classifier = RandomForestClassifier(n_estimators = 200, max_features = 10,
										 max_depth = None, min_samples_split = 1, 
										 verbose = 1)
	rf_classifier.fit(X_train, y_train)
	y_prob = rf_classifier.predict_proba(X_test)
	y_pred = y_prob[:,1]
	return y_pred

def extremely_random_forest(X_train, y_train, X_test):
	erf_classifier = ExtraTreesClassifier(n_estimators=500, max_depth=None, 
							min_samples_split=1, random_state=0, verbose = 1)
	erf_classifier.fit(X_train,y_train)
	y_prob = erf_classifier.predict_proba(X_test)
	y_pred = y_prob[:,1]
	return y_pred

def extra_random_forest(X_train, y_train, X_test):
	extra_classifier = ExtraTreesClassifier(n_estimators=500, max_depth=None, 
							min_samples_split=1, random_state=0, verbose = 1)
	extra_classifier.fit(X_train,y_train)
	y_prob = extra_classifier.predict_proba(X_test)
	y_pred = y_prob[:,1]
	return y_pred

def gbrt(X_train, y_train, X_test):
	gbrt_classifier = GradientBoostingClassifier(loss = 'exponential', 
											n_estimators=150, max_depth = 8, 
											learning_rate = 0.1, verbose = 1, 
											min_samples_split=8, min_samples_leaf=700)
	gbrt_classifier.fit(X_train, y_train)	
	y_prob = gbrt_classifier.predict_proba(X_test)
	y_pred = y_prob[:,1]
	print gbrt_classifier.get_params(deep = False)
	return y_pred

def tune_parameter(X_train, y_trains):
	#http://scikit-learn.org/stable/modules/generated/sklearn.grid_search.GridSearchCV.html#sklearn.grid_search.GridSearchCV
	from sklearn.grid_search import GridSearchCV
	param_grid = {'learning_rate': [0.1, 0.01],
              'max_depth': [4, 6, 10], 
              'min_samples_leaf': [2,10,50,100,200], 
              'min_samples_split': [1,5,10,15,20]
              }
	est = GradientBoostingClassifier(n_estimators=50)
	gs_cv = GridSearchCV(est, param_grid, cv = 5, n_jobs=4, verbose = 1).fit(X_train, y_train)
	print gs_cv.best_params_

	# regressor when n_es = 100, the output: {'learning_rate': 0.05, 'max_depth': 6, 'min_samples_leaf': 17}
	# classifier when n_es = 50, {'max_features': 0.1, 'learning_rate': 0.02, 'random_state': 1, 'max_depth': 10, 'min_samples_leaf': 5}

def gbrt_bash(X_train, y_train, X_test, y_test):
	original_params = {'n_estimators': 150, 'verbose': 1}

	loss_para = ['deviance'] # when set to exponential, equals adaboost
	learning_rate = [0.1] # leaning rate is a drade-off with nestimators
	max_depth = [5,8,10,15]#[10, 50, 100] # this is eaqual to set max_leaf_nodes
	subsample_fraction = [1.0]#[0.5,1.0] #The fraction of samples to be used for fitting the individual base learners
	min_samples_leaf = [200,300,800,900,1000]#[2,4,10] #8
	min_samples_split = [8,10,12,20]#[10,50,100] #50

	settings = []
	for loss in loss_para:
		for rate in learning_rate:
			for depth in max_depth:
				for subsample in subsample_fraction:
					for samples_leaf in min_samples_leaf:
						for samples_split in min_samples_split:
							settings.append({'loss':loss, 'learning_rate': rate, 
								'max_depth': depth, 'subsample':subsample, 
								'min_samples_split':samples_split, 'min_samples_leaf':samples_leaf})

	for setting in settings:
		params = dict(original_params)
		params.update(setting)
		clf = GradientBoostingClassifier(**params)
		clf.fit(X_train, y_train)
		y_prob = clf.predict_proba(X_test)
		y_pred = y_prob[:,1]
		print setting
		print offline_score(y_test, y_pred)

def gbrt_multi(min_samples_split_setting):
	gbrt_classifier = GradientBoostingClassifier(loss = 'exponential', 
											n_estimators = 150, max_depth = 8, 
											learning_rate = 0.1, verbose = 1, 
											min_samples_split = min_samples_split_setting, 
											min_samples_leaf = 700)	
	gbrt_classifier.fit(X_train, y_train)
	y_prob = gbrt_classifier.predict_proba(X_test)
	y_pred = y_prob[:,1]
	return y_pred

def multi_processing():
	from multiprocessing import Pool
	p = Pool(16)
    print(p.map(gbrt_multi, [1, 5, 10]))

if __name__ == '__main__':
	X_train_raw, y_train, X_test_raw, y_test = load_svmlight_files(("data/feature/train_gh_52_20_1","data/feature/train_gh_52_20_2"))
	X_train = X_train_raw.toarray()
	X_test = X_test_raw.toarray()

	y_pred = gbrt(X_train, y_train, X_test)
	
	#tune_parameter(X_train,y_train)
	#gbrt_bash(X_train,y_train,X_test,y_test)


	print offline_score(y_test, y_pred)
	#write_file(y_pred, 'yz_37_14')







