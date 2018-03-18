from copy import deepcopy
import pandas as pd
from data_encoding import one_hot, binary_vectorizing, ternary_vectorizing
from sklearn import svm, preprocessing
from sklearn.metrics import confusion_matrix
import sklearn.linear_model as lm
import numpy as np
import itertools
import matplotlib.pyplot as plt
from sklearn.base import clone
from optparse import OptionParser



LOG_FILE = "log_final.txt"
log = open(LOG_FILE, 'w+')

def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')


def run_model(train_file_name, models):
    BANK_TRAINING = train_file_name

    # BANK_TRAINING = "bank-training_new.csv"
    BANK_TESTING = "./dataAnalysis/bank-testing_new.csv"

    COLUMNS = ["age", "job", "marital", "education", "default", "balance",
               "housing", "loan", "contact", "day", "month", "duration",
               "campaign", "pdays", "previous", "poutcome", "y"]
    CATEGORICAL_COLUMNS = ["job", "marital", "education", "default", "housing",
                           "loan", "contact", "day", "month", "poutcome"]
    CONTINUOUS_COLUMNS = ["age", "balance", "duration", "campaign", "pdays",
                          "previous"]
    CATEGORICAL_COLUMNS_2 = ["default", "housing", "loan", "day", "month",
                             "poutcome"]
    LABEL = "y"

    standard_scaler = preprocessing.StandardScaler()

    ############################
    training_set = pd.read_csv(BANK_TRAINING, names=COLUMNS,
                               skipinitialspace=True, skiprows=1)
    training_label_set = deepcopy(training_set[LABEL])
    del training_set[LABEL]

    #
    training_set_imputed = deepcopy(training_set)
    training_set_imputed = training_set_imputed.drop(
        ['marital', 'job', 'contact'], axis=1)
    training_set_imputed['education'] = ternary_vectorizing(
        training_set_imputed['education'], ['primary', 'secondary', 'tertiary'])
    training_set_imputed['education'].replace('unknown', np.nan, inplace=True)
    training_set_imputed.fillna(training_set_imputed.mean(), inplace=True)
    training_set_imputed = one_hot(training_set_imputed, CATEGORICAL_COLUMNS_2)
    #
    training_label_set = binary_vectorizing(training_label_set, ['no', 'yes'])
    #
    training_set_sc_scaled_imputed = standard_scaler.fit_transform(
        training_set_imputed)
    training_set_sc_scaled_imputed = pd.DataFrame(
        training_set_sc_scaled_imputed)
    #

    ##########################
    validation_set = pd.read_csv(BANK_TESTING, names=COLUMNS,
                                 skipinitialspace=True, skiprows=1)
    validation_label_set = deepcopy(validation_set[LABEL])
    del validation_set[LABEL]

    #
    validation_set_imputed = deepcopy(validation_set)
    validation_set_imputed = validation_set_imputed.drop(
        ['marital', 'job', 'contact'], axis=1)
    validation_set_imputed['education'] = ternary_vectorizing(
        validation_set_imputed['education'],
        ['primary', 'secondary', 'tertiary'])
    validation_set_imputed['education'].replace('unknown', np.nan, inplace=True)
    validation_set_imputed.fillna(validation_set_imputed.mean(), inplace=True)
    validation_set_imputed = one_hot(validation_set_imputed,
                                     CATEGORICAL_COLUMNS_2)
    #
    validation_label_set = binary_vectorizing(validation_label_set,
                                              ['no', 'yes'])
    #
    validation_set_sc_scaled_imputed = standard_scaler.fit_transform(
        validation_set_imputed)
    validation_set_sc_scaled_imputed = pd.DataFrame(
        validation_set_sc_scaled_imputed)
    #





    #####################################################################
    # Array of Tuples of Model,Training Data, Validation Data, Description
    pipelines = {}

    pipelines['lm'] = (lm.LogisticRegression(), training_set_sc_scaled_imputed,
                       validation_set_sc_scaled_imputed,
                       "Imputed->Standard-Scaled->Logistic Regression")

    pipelines['svm'] = (svm.SVC(kernel='rbf', degree=16, max_iter=100),
                        training_set_sc_scaled_imputed,
                        validation_set_sc_scaled_imputed,
                        "Imputed->Standard-Scaled->16RBF Support Vector Machine")

    result = {}
    for model_name in models:
        print model_name
        pipeline = pipelines[model_name]
        mdl, train, validate, description = pipeline
        print description

        #Sci-Kit Learn Model

        fit_model = mdl.fit(train, training_label_set) \

        label_pred = fit_model.predict(validate)
        # Compute confusion matrix
        cnf_matrix = confusion_matrix(validation_label_set, label_pred)
        np.set_printoptions(precision=2)
        #
        # # Plot non-normalized confusion matrix
        # plt.figure()
        # plot_confusion_matrix(cnf_matrix, classes=['no', 'yes'],
        #                       title='Confusion matrix, without normalization')
        result[model_name] = cnf_matrix
        print model_name, cnf_matrix
        return result


def main():
    parser = OptionParser()
    parser.add_option('--models', dest='models', action="append", type="str")

    (options, args) = parser.parse_args()
    run_model('', options.models)


if __name__ == '__main__':
    main()

#####################################################################
# f = open(LOG_FILE, 'w+')
#
# for pipeline in pipelines:
#
#     mdl, train, validate, description = pipeline
#     print description
#
#     #Sci-Kit Learn Model
#
#     fit_model = mdl.fit(train, training_label_set) \
#
#     label_pred = fit_model.predict(validate)
#
#
#
#     # Compute confusion matrix
#     cnf_matrix = confusion_matrix(validation_label_set, label_pred)
#     np.set_printoptions(precision=2)
#
#     # Plot non-normalized confusion matrix
#     plt.figure()
#     plot_confusion_matrix(cnf_matrix, classes=['no', 'yes'],
#                           title='Confusion matrix, without normalization')
#
#     # Plot normalized confusion matrix
#     plt.figure()
#     plot_confusion_matrix(cnf_matrix, classes=['no', 'yes'], normalize=True,
#                           title='Normalized confusion matrix')
#
#     plt.show()
#
# f.close()
