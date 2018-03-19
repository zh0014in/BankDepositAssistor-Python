from copy import deepcopy
import pandas as pd
from data_encoding import one_hot, binary_vectorizing, ternary_vectorizing
from sklearn import svm, tree, preprocessing
from sklearn.decomposition import PCA, IncrementalPCA
from sklearn.ensemble import RandomForestClassifier
import sklearn.linear_model as lm
import sklearn.neighbors as knn
import tensorflow.contrib.learn as learn
from tensorflow.contrib import layers
import numpy as np


BANK_TRAINING = "bank-training_new.csv"
BANK_VALIDATION = "bank-crossvalidation_new.csv"
LOG_FILE = "log.txt"

COLUMNS = ["age","job","marital","education","default","balance","housing","loan","contact","day","month","duration",
           "campaign","pdays","previous","poutcome","y"]
CATEGORICAL_COLUMNS = ["job","marital","education","default","housing","loan","contact","day","month","poutcome"]
CONTINUOUS_COLUMNS = ["age","balance","duration","campaign","pdays","previous"]
CATEGORICAL_COLUMNS_2 = ["default","housing","loan","day","month","poutcome"]
LABEL = "y"

min_max_scaler = preprocessing.MinMaxScaler()
standard_scaler = preprocessing.StandardScaler()
pca = PCA(n_components=5)
ipca = IncrementalPCA(n_components=5)

############################
training_set = pd.read_csv(BANK_TRAINING, names=COLUMNS, skipinitialspace=True, skiprows=1)
training_label_set = deepcopy(training_set[LABEL])
del training_set[LABEL]

#
training_set_imputed = deepcopy(training_set)
training_set_imputed = training_set_imputed.drop(['marital', 'job', 'contact'], axis=1)
training_set_imputed['education'] = ternary_vectorizing(training_set_imputed['education'], ['primary', 'secondary', 'tertiary'])
training_set_imputed['education'].replace('unknown', np.nan, inplace=True)
training_set_imputed.fillna(training_set_imputed.mean(), inplace=True)
training_set_imputed = one_hot(training_set_imputed, CATEGORICAL_COLUMNS_2)
#
training_set = one_hot(training_set, CATEGORICAL_COLUMNS)
training_label_set = binary_vectorizing(training_label_set, ['no', 'yes'])
#
training_set_mn_scaled = min_max_scaler.fit_transform(training_set)
training_set_mn_scaled = pd.DataFrame(training_set_mn_scaled)
#
training_set_sc_scaled = standard_scaler.fit_transform(training_set)
training_set_sc_scaled = pd.DataFrame(training_set_sc_scaled)
#
training_set_pca_sc_scaled = ipca.fit_transform(deepcopy(training_set_sc_scaled))
#
training_set_mn_scaled_imputed = min_max_scaler.fit_transform(training_set_imputed)
training_set_mn_scaled_imputed = pd.DataFrame(training_set_mn_scaled_imputed)
#
training_set_sc_scaled_imputed = standard_scaler.fit_transform(training_set_imputed)
training_set_sc_scaled_imputed = pd.DataFrame(training_set_sc_scaled_imputed)
#
training_set_pca_sc_scaled_imputed = ipca.fit_transform(deepcopy(training_set_sc_scaled_imputed))

##########################
validation_set = pd.read_csv(BANK_VALIDATION, names=COLUMNS, skipinitialspace=True, skiprows=1)
validation_label_set = deepcopy(validation_set[LABEL])
del validation_set[LABEL]

#
validation_set_imputed = deepcopy(validation_set)
validation_set_imputed = validation_set_imputed.drop(['marital', 'job', 'contact'], axis=1)
validation_set_imputed['education'] = ternary_vectorizing(validation_set_imputed['education'], ['primary', 'secondary', 'tertiary'])
validation_set_imputed['education'].replace('unknown', np.nan, inplace=True)
validation_set_imputed.fillna(validation_set_imputed.mean(), inplace=True)
validation_set_imputed = one_hot(validation_set_imputed, CATEGORICAL_COLUMNS_2)
#
validation_set = one_hot(validation_set, CATEGORICAL_COLUMNS)
validation_label_set = binary_vectorizing(validation_label_set, ['no', 'yes'])
#
validation_set_mn_scaled = min_max_scaler.fit_transform(validation_set)
validation_set_mn_scaled = pd.DataFrame(validation_set_mn_scaled)
#
validation_set_sc_scaled = standard_scaler.fit_transform(validation_set)
validation_set_sc_scaled = pd.DataFrame(validation_set_sc_scaled)
#
validation_set_pca_sc_scaled = ipca.fit_transform(deepcopy(validation_set_sc_scaled))
#
validation_set_mn_scaled_imputed = min_max_scaler.fit_transform(validation_set_imputed)
validation_set_mn_scaled_imputed = pd.DataFrame(validation_set_mn_scaled_imputed)
#
validation_set_sc_scaled_imputed = standard_scaler.fit_transform(validation_set_imputed)
validation_set_sc_scaled_imputed = pd.DataFrame(validation_set_sc_scaled_imputed)
#
validation_set_pca_sc_scaled_imputed = ipca.fit_transform(deepcopy(validation_set_sc_scaled_imputed))

#####################################################################
#Array of Tuples of Model,Training Data, Validation Data, Description
pipelines = []

pipelines.append((lm.LogisticRegression(), training_set, validation_set, "Logistic Regression"))
pipelines.append((lm.LogisticRegression(), training_set_mn_scaled, validation_set_mn_scaled, "MinMax-Scaled->Logistic Regression"))
pipelines.append((lm.LogisticRegression(), training_set_sc_scaled, validation_set_sc_scaled, "Standard-Scaled->Logistic Regression"))
pipelines.append((lm.LogisticRegression(), training_set_pca_sc_scaled, validation_set_pca_sc_scaled, "Standard-Scaled->PCA->Logistic Regression"))
pipelines.append((lm.LogisticRegression(), training_set_imputed, validation_set_imputed, "Imputed Logistic Regression"))
pipelines.append((lm.LogisticRegression(), training_set_mn_scaled_imputed, validation_set_mn_scaled_imputed, "Imputed->MinMax-Scaled->Logistic Regression"))
pipelines.append((lm.LogisticRegression(), training_set_sc_scaled_imputed, validation_set_sc_scaled_imputed, "Imputed->Standard-Scaled->Logistic Regression"))
pipelines.append((lm.LogisticRegression(), training_set_pca_sc_scaled_imputed, validation_set_pca_sc_scaled_imputed, "Imputed->Standard-Scaled->PCA->Logistic Regression"))


pipelines.append((knn.KNeighborsClassifier(), training_set, validation_set, "K-Nearest Neighbours"))
pipelines.append((knn.KNeighborsClassifier(), training_set_mn_scaled, validation_set_mn_scaled, "MinMax-Scaled->K-Nearest Neighbours"))
pipelines.append((knn.KNeighborsClassifier(), training_set_sc_scaled, validation_set_sc_scaled, "Standard-Scaled->K-Nearest Neighbours"))
pipelines.append((knn.KNeighborsClassifier(), training_set_pca_sc_scaled, validation_set_pca_sc_scaled, "Standard-Scaled->PCA->K-Nearest Neighbours"))
pipelines.append((knn.KNeighborsClassifier(), training_set_imputed, validation_set_imputed, "Imputed->K-Nearest Neighbours"))
pipelines.append((knn.KNeighborsClassifier(), training_set_mn_scaled_imputed, validation_set_mn_scaled_imputed, "Imputed->MinMax-Scaled->K-Nearest Neighbours"))
pipelines.append((knn.KNeighborsClassifier(), training_set_sc_scaled_imputed, validation_set_sc_scaled_imputed, "Imputed->Standard-Scaled->K-Nearest Neighbours"))
pipelines.append((knn.KNeighborsClassifier(), training_set_pca_sc_scaled_imputed, validation_set_pca_sc_scaled_imputed, "Imputed->Standard-Scaled->PCA->K-Nearest Neighbours"))


pipelines.append((svm.SVC(kernel='linear',  max_iter=1000000), training_set, validation_set, "Linear Support Vector Machine"))
pipelines.append((svm.SVC(kernel='linear',  max_iter=1000000), training_set_mn_scaled, validation_set_mn_scaled, "MinMax-Scaled->Linear Support Vector Machine"))
pipelines.append((svm.SVC(kernel='linear',  max_iter=1000000), training_set_sc_scaled, validation_set_sc_scaled, "Standard-Scaled->Linear Support Vector Machine"))
pipelines.append((svm.SVC(kernel='linear',  max_iter=1000000), training_set_pca_sc_scaled, validation_set_pca_sc_scaled, "Standard-Scaled->PCA->Linear Support Vector Machine"))
pipelines.append((svm.SVC(kernel='linear',  max_iter=1000000), training_set_imputed, validation_set_imputed, "Imputed->Linear Support Vector Machine"))
pipelines.append((svm.SVC(kernel='linear',  max_iter=1000000), training_set_mn_scaled_imputed, validation_set_mn_scaled_imputed, "Imputed->MinMax-Scaled->Linear Support Vector Machine"))
pipelines.append((svm.SVC(kernel='linear',  max_iter=1000000), training_set_sc_scaled_imputed, validation_set_sc_scaled_imputed, "Imputed->Standard-Scaled->Linear Support Vector Machine"))
pipelines.append((svm.SVC(kernel='linear',  max_iter=1000000), training_set_pca_sc_scaled_imputed, validation_set_pca_sc_scaled_imputed, "Imputed->Standard-Scaled->PCA->Linear Support Vector Machine"))


pipelines.append((svm.SVC(kernel='poly', degree=3,  max_iter=1000000), training_set, validation_set, "3Poly Support Vector Machine"))
pipelines.append((svm.SVC(kernel='poly', degree=3,  max_iter=1000000), training_set_mn_scaled, validation_set_mn_scaled, "MinMax-Scaled->3Poly Support Vector Machine"))
pipelines.append((svm.SVC(kernel='poly', degree=3,  max_iter=1000000), training_set_sc_scaled, validation_set_sc_scaled, "Standard-Scaled->3Poly Support Vector Machine"))
pipelines.append((svm.SVC(kernel='poly', degree=3,  max_iter=1000000), training_set_pca_sc_scaled, validation_set_pca_sc_scaled, "Standard-Scaled->PCA->3Poly Support Vector Machine"))
pipelines.append((svm.SVC(kernel='poly', degree=3,  max_iter=1000000), training_set_imputed, validation_set_imputed, "Imputed->3Poly Support Vector Machine"))
pipelines.append((svm.SVC(kernel='poly', degree=3,  max_iter=1000000), training_set_mn_scaled_imputed, validation_set_mn_scaled_imputed, "Imputed->MinMax-Scaled->3Poly Support Vector Machine"))
pipelines.append((svm.SVC(kernel='poly', degree=3,  max_iter=1000000), training_set_sc_scaled_imputed, validation_set_sc_scaled_imputed, "Imputed->Standard-Scaled->3Poly Support Vector Machine"))
pipelines.append((svm.SVC(kernel='poly', degree=3,  max_iter=1000000), training_set_pca_sc_scaled_imputed, validation_set_pca_sc_scaled_imputed, "Imputed->Standard-Scaled->PCA->3Poly Support Vector Machine"))


pipelines.append((svm.SVC(kernel='poly', degree=16,  max_iter=1000000), training_set, validation_set, "16Poly Support Vector Machine"))
pipelines.append((svm.SVC(kernel='poly', degree=16,  max_iter=1000000), training_set_mn_scaled, validation_set_mn_scaled, "MinMax-Scaled->16Poly Support Vector Machine"))
pipelines.append((svm.SVC(kernel='poly', degree=16,  max_iter=1000000), training_set_sc_scaled, validation_set_sc_scaled, "Standard-Scaled->16Poly Support Vector Machine"))
pipelines.append((svm.SVC(kernel='poly', degree=16,  max_iter=1000000), training_set_pca_sc_scaled, validation_set_pca_sc_scaled, "Standard-Scaled->PCA->16Poly Support Vector Machine"))
pipelines.append((svm.SVC(kernel='poly', degree=16,  max_iter=1000000), training_set_imputed, validation_set_imputed, "Imputed->16Poly Support Vector Machine"))
pipelines.append((svm.SVC(kernel='poly', degree=16,  max_iter=1000000), training_set_mn_scaled_imputed, validation_set_mn_scaled_imputed, "Imputed->MinMax-Scaled->16Poly Support Vector Machine"))
pipelines.append((svm.SVC(kernel='poly', degree=16,  max_iter=1000000), training_set_sc_scaled_imputed, validation_set_sc_scaled_imputed, "Imputed->Standard-Scaled->16Poly Support Vector Machine"))
pipelines.append((svm.SVC(kernel='poly', degree=16,  max_iter=1000000), training_set_pca_sc_scaled_imputed, validation_set_pca_sc_scaled_imputed, "Imputed->Standard-Scaled->PCA->16Poly Support Vector Machine"))



pipelines.append((svm.SVC(kernel='rbf', degree=16,  max_iter=1000000), training_set, validation_set, "16RBF Support Vector Machine"))
pipelines.append((svm.SVC(kernel='rbf', degree=16,  max_iter=1000000), training_set_mn_scaled, validation_set_mn_scaled, "MinMax-Scaled->16RBF Support Vector Machine"))
pipelines.append((svm.SVC(kernel='rbf', degree=16,  max_iter=1000000), training_set_sc_scaled, validation_set_sc_scaled, "Standard-Scaled->16RBF Support Vector Machine"))
pipelines.append((svm.SVC(kernel='rbf', degree=16,  max_iter=1000000), training_set_pca_sc_scaled, validation_set_pca_sc_scaled, "Standard-Scaled->PCA->16RBF Support Vector Machine"))
pipelines.append((svm.SVC(kernel='rbf', degree=16,  max_iter=1000000), training_set_imputed, validation_set_imputed, "Imputed->16RBF Support Vector Machine"))
pipelines.append((svm.SVC(kernel='rbf', degree=16,  max_iter=1000000), training_set_mn_scaled_imputed, validation_set_mn_scaled_imputed, "Imputed->MinMax-Scaled->16RBF Support Vector Machine"))
pipelines.append((svm.SVC(kernel='rbf', degree=16,  max_iter=1000000), training_set_sc_scaled_imputed, validation_set_sc_scaled_imputed, "Imputed->Standard-Scaled->16RBF Support Vector Machine"))
pipelines.append((svm.SVC(kernel='rbf', degree=16,  max_iter=1000000), training_set_pca_sc_scaled_imputed, validation_set_pca_sc_scaled_imputed, "Imputed->Standard-Scaled->PCA->16RBF Support Vector Machine"))


pipelines.append((tree.DecisionTreeClassifier(), training_set, validation_set, "Decision Tree"))
pipelines.append((tree.DecisionTreeClassifier(), training_set_mn_scaled, validation_set_mn_scaled, "MinMax-Scaled->Decision Tree"))
pipelines.append((tree.DecisionTreeClassifier(), training_set_sc_scaled, validation_set_sc_scaled, "Standard-Scaled->Decision Tree"))
pipelines.append((tree.DecisionTreeClassifier(), training_set_pca_sc_scaled, validation_set_pca_sc_scaled, "Standard-Scaled->PCA->Decision Tree"))
pipelines.append((tree.DecisionTreeClassifier(), training_set_imputed, validation_set_imputed, "Imputed->Decision Tree"))
pipelines.append((tree.DecisionTreeClassifier(), training_set_mn_scaled_imputed, validation_set_mn_scaled_imputed, "Imputed->MinMax-Scaled->Decision Tree"))
pipelines.append((tree.DecisionTreeClassifier(), training_set_sc_scaled_imputed, validation_set_sc_scaled_imputed, "Imputed->Standard-Scaled->Decision Tree"))
pipelines.append((tree.DecisionTreeClassifier(), training_set_pca_sc_scaled_imputed, validation_set_pca_sc_scaled_imputed, "Imputed->Standard-Scaled->PCA->Decision Tree"))



pipelines.append((RandomForestClassifier(), training_set, validation_set, "Random Forest"))
pipelines.append((RandomForestClassifier(), training_set_mn_scaled, validation_set_mn_scaled, "MinMax-Scaled->Random Forest"))
pipelines.append((RandomForestClassifier(), training_set_sc_scaled, validation_set_sc_scaled, "Standard-Scaled->Random Forest"))
pipelines.append((RandomForestClassifier(), training_set_pca_sc_scaled, validation_set_pca_sc_scaled, "Standard-Scaled->PCA->Random Forest"))
pipelines.append((RandomForestClassifier(), training_set_imputed, validation_set_imputed, "Imputed->Random Forest"))
pipelines.append((RandomForestClassifier(), training_set_mn_scaled_imputed, validation_set_mn_scaled_imputed, "Imputed->MinMax-Scaled->Random Forest"))
pipelines.append((RandomForestClassifier(), training_set_sc_scaled_imputed, validation_set_sc_scaled_imputed, "Imputed->Standard-Scaled->Random Forest"))
pipelines.append((RandomForestClassifier(), training_set_pca_sc_scaled_imputed, validation_set_pca_sc_scaled_imputed, "Imputed->Standard-Scaled->PCA->Random Forest"))


fc = [layers.real_valued_column("", dimension=len(training_set.columns))]
classifier_lc = learn.LinearClassifier(feature_columns=fc, n_classes=2)
classifier_dlc = learn.DNNLinearCombinedClassifier(linear_feature_columns=fc, n_classes=2)
classifier_dc = learn.DNNClassifier(feature_columns=fc, n_classes=2, hidden_units=[1000,300,200])

fc_imputed = [layers.real_valued_column("", dimension=len(training_set_imputed.columns))]
classifier_lc_imputed = learn.LinearClassifier(feature_columns=fc_imputed, n_classes=2)
classifier_dlc_imputed = learn.DNNLinearCombinedClassifier(linear_feature_columns=fc_imputed , n_classes=2)
classifier_dc_imputed = learn.DNNClassifier(feature_columns=fc_imputed, n_classes=2, hidden_units=[1000,300,200])


fc_pca = [layers.real_valued_column("", dimension=len(training_set_pca_sc_scaled.columns))]
classifier_lc_pca = learn.LinearClassifier(feature_columns=fc_pca, n_classes=2)
classifier_dlc_pca = learn.DNNLinearCombinedClassifier(linear_feature_columns=fc_pca, n_classes=2)
classifier_dc_pca = learn.DNNClassifier(feature_columns=fc_pca, n_classes=2, hidden_units=[1000,300,200])


pipelines.append((classifier_lc, training_set, validation_set, "* Linear"))
pipelines.append((classifier_dlc, training_set, validation_set, "* Deep Mixed Linear"))
pipelines.append((classifier_dc, training_set, validation_set, "* Deep Neural"))

pipelines.append((classifier_lc, training_set_mn_scaled, validation_set_mn_scaled, "* MinMax-Scaled->Linear"))
pipelines.append((classifier_dlc, training_set_mn_scaled, validation_set_mn_scaled, "* MinMax-Scaled->Deep Mixed Linear"))
pipelines.append((classifier_dc, training_set_mn_scaled, validation_set_mn_scaled, "* MinMax-Scaled->Deep Neural"))

pipelines.append((classifier_lc, training_set_sc_scaled, validation_set_sc_scaled, "* Standard-Scaled->Linear"))
pipelines.append((classifier_dlc, training_set_sc_scaled, validation_set_sc_scaled, "* Standard-Scaled->Deep Mixed Linear"))
pipelines.append((classifier_dc, training_set_sc_scaled, validation_set_sc_scaled, "* Standard-Scaled->Deep Neural"))

pipelines.append((classifier_lc_pca, training_set_pca_sc_scaled, validation_set_pca_sc_scaled, "* Standard-Scaled->PCA->Linear"))
pipelines.append((classifier_dlc_pca, training_set_pca_sc_scaled, validation_set_pca_sc_scaled, "* Standard-Scaled->PCA->Deep Mixed Linear"))
pipelines.append((classifier_dc_pca, training_set_pca_sc_scaled, validation_set_pca_sc_scaled, "* Standard-Scaled->PCA->Deep Neural"))

##
pipelines.append((classifier_lc_imputed, training_set_imputed, validation_set_imputed, "* Imputed->Linear"))
pipelines.append((classifier_dlc_imputed, training_set_imputed, validation_set_imputed, "* Imputed->Deep Mixed Linear"))
pipelines.append((classifier_dc_imputed, training_set_imputed, validation_set_imputed, "* Imputed->Deep Neural"))

pipelines.append((classifier_lc_imputed, training_set_mn_scaled_imputed, validation_set_mn_scaled_imputed, "* Imputed->MinMax-Scaled->Linear"))
pipelines.append((classifier_dlc_imputed, training_set_mn_scaled_imputed, validation_set_mn_scaled_imputed, "* Imputed->MinMax-Scaled->Deep Mixed Linear"))
pipelines.append((classifier_dc_imputed, training_set_mn_scaled_imputed, validation_set_mn_scaled_imputed, "* Imputed->MinMax-Scaled->Deep Neural"))

pipelines.append((classifier_lc_imputed, training_set_sc_scaled_imputed, validation_set_sc_scaled_imputed, "* Imputed->Standard-Scaled->Linear"))
pipelines.append((classifier_dlc_imputed, training_set_sc_scaled_imputed, validation_set_sc_scaled_imputed, "* Imputed->Standard-Scaled->Deep Mixed Linear"))
pipelines.append((classifier_dc_imputed, training_set_sc_scaled_imputed, validation_set_sc_scaled_imputed, "* Imputed->Standard-Scaled->Deep Neural"))

pipelines.append((classifier_lc_imputed, training_set_pca_sc_scaled_imputed, validation_set_pca_sc_scaled_imputed, "* Imputed->Standard-Scaled->PCA->Linear"))
pipelines.append((classifier_dlc_imputed, training_set_pca_sc_scaled_imputed, validation_set_pca_sc_scaled_imputed, "* Imputed->Standard-Scaled->PCA->Deep Mixed Linear"))
pipelines.append((classifier_dc_imputed, training_set_pca_sc_scaled_imputed, validation_set_pca_sc_scaled_imputed, "* Imputed->Standard-Scaled->PCA->Deep Neural"))


#####################################################################
f = open(LOG_FILE, 'w+')

for pipeline in pipelines:

    mdl, train, validate, description = pipeline
    if description[0] == '*':
        #Tensorflow Model
        mdl.fit(x=train, y=training_label_set, steps=10)
        score = str( mdl.evaluate(x=validate, y=validation_label_set)['accuracy'] )
    else:
        #Sci-Kit Learn Model
        mdl.fit(train, training_label_set)
        score = str( mdl.score(validate, validation_label_set) )

    describe = description +"  "+ score + "\n\n**********\n\n"
    f.write(describe)
    print(describe)

f.close()