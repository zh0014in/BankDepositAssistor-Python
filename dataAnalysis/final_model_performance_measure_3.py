from copy import deepcopy
import pandas as pd
from data_encoding import one_hot, binary_vectorizing, ternary_vectorizing
from sklearn import svm, preprocessing
from sklearn.metrics import confusion_matrix
import sklearn.linear_model as lm
import numpy as np
import csv
import itertools
# import matplotlib.pyplot as plt
from sklearn.base import clone
from optparse import OptionParser
import pickle
from sklearn.externals import joblib

# LOG_FILE = "log_final.txt"
# log = open(LOG_FILE, 'w+')

# def plot_confusion_matrix(cm, classes,
#                           normalize=False,
#                           title='Confusion matrix',
#                           cmap=plt.cm.Blues):
#     """
#     This function prints and plots the confusion matrix.
#     Normalization can be applied by setting `normalize=True`.
#     """
#     plt.imshow(cm, interpolation='nearest', cmap=cmap)
#     plt.title(title)
#     plt.colorbar()
#     tick_marks = np.arange(len(classes))
#     plt.xticks(tick_marks, classes, rotation=45)
#     plt.yticks(tick_marks, classes)
#
#     if normalize:
#         cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
#         print("Normalized confusion matrix")
#     else:
#         print('Confusion matrix, without normalization')
#
#     print(cm)
#
#     thresh = cm.max() / 2.
#     for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
#         plt.text(j, i, cm[i, j],
#                  horizontalalignment="center",
#                  color="white" if cm[i, j] > thresh else "black")
#
#     plt.tight_layout()
#     plt.ylabel('True label')
#     plt.xlabel('Predicted label')

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

MODELS = {
    'lm': lm.LogisticRegression(),
    'svm': svm.SVC(kernel='rbf', degree=16, max_iter=100)
}


def run_model(model_name, train_or_predict,
              train_file_name='bank-training_new.csv',
              validate_file_name='bank-training_new.csv',
              predict_file_name='bank-training_new.csv'):

    def train():
        ############################
        training_set = pd.read_csv(train_file_name, names=COLUMNS,
                                   skipinitialspace=True, skiprows=1)
        training_label_set = deepcopy(training_set[LABEL])
        del training_set[LABEL]

        training_set_imputed = deepcopy(training_set)
        training_set_imputed = training_set_imputed.drop(
            ['marital', 'job', 'contact'], axis=1)
        training_set_imputed['education'] = ternary_vectorizing(
            training_set_imputed['education'],
            ['primary', 'secondary', 'tertiary'])
        training_set_imputed['education'].replace('unknown', np.nan,
                                                  inplace=True)
        training_set_imputed.fillna(training_set_imputed.mean(), inplace=True)
        training_set_imputed = one_hot(training_set_imputed,
                                       CATEGORICAL_COLUMNS_2)
        #
        training_label_set = binary_vectorizing(training_label_set,
                                                ['no', 'yes'])
        #
        training_set_sc_scaled_imputed = standard_scaler.fit_transform(
            training_set_imputed)
        training_set_sc_scaled_imputed = pd.DataFrame(
            training_set_sc_scaled_imputed)

        fit_model = MODELS[model_name].fit(training_set_sc_scaled_imputed,
                                           training_label_set)

        joblib.dump(fit_model, model_file_name)
        if 'predict' not in train_or_predict and 'validate' not in train_or_predict:
            print model_name, model_file_name
            return model_name, model_file_name

    def validate():
        print 123
        fit_model = joblib.load(model_file_name)

        validation_set = pd.read_csv(validate_file_name, names=COLUMNS,
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
        validation_set_imputed['education'].replace('unknown', np.nan,
                                                    inplace=True)
        validation_set_imputed.fillna(validation_set_imputed.mean(),
                                      inplace=True)
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

        print 'validation_set_sc_scaled_imputed', list(
            validation_set_sc_scaled_imputed.columns.values)

        label_pred = fit_model.predict(validation_set_sc_scaled_imputed)

        cnf_matrix = confusion_matrix(validation_label_set, label_pred)
        np.set_printoptions(precision=2)
        print model_name, cnf_matrix
        if 'predict' not in train_or_predict:
            return model_name, cnf_matrix

    def predict():
        print 123
        fit_model = joblib.load(model_file_name)

        predict_set = pd.read_csv(predict_file_name, names=COLUMNS,
                                  skipinitialspace=True, skiprows=1)
        validation_label_set = deepcopy(predict_set[LABEL])
        del predict_set[LABEL]

        #
        predict_set_imputed = deepcopy(predict_set)
        predict_set_imputed = predict_set_imputed.drop(
            ['marital', 'job', 'contact'], axis=1)
        predict_set_imputed['education'] = ternary_vectorizing(
            predict_set_imputed['education'],
            ['primary', 'secondary', 'tertiary'])
        predict_set_imputed['education'].replace('unknown', np.nan,
                                                 inplace=True)
        predict_set_imputed.fillna(predict_set_imputed.mean(),
                                   inplace=True)
        predict_set_imputed = one_hot(predict_set_imputed,
                                      CATEGORICAL_COLUMNS_2)
        #
        # validation_label_set = binary_vectorizing(validation_label_set,
        #                                           ['no', 'yes'])
        #
        predict_set_sc_scaled_imputed = standard_scaler.fit_transform(
            predict_set_imputed)
        predict_set_sc_scaled_imputed = pd.DataFrame(
            predict_set_sc_scaled_imputed)

        print 'predict_set_sc_scaled_imputed', list(
            predict_set_sc_scaled_imputed.columns.values)

        label_pred = fit_model.predict(predict_set_sc_scaled_imputed)
        i = 0
        label_pred = ['result'] + label_pred.tolist()
        with open(predict_file_name, 'r') as csvinput:
            with open('result_' + predict_file_name, 'w') as csvoutput:
                writer = csv.writer(csvoutput)
                for row in csv.reader(csvinput):
                    writer.writerow(row + [str(label_pred[i])])
                    i += 1

        return model_name, 'result_' + predict_file_name

    assert model_name is not None
    assert train_or_predict is not None

    model_file_name = model_name + '.pkl'
    print train_or_predict
    standard_scaler = preprocessing.StandardScaler()

    if 'train' in train_or_predict:
        train()

    print 2
    if 'validate' in train_or_predict:
        validate()

    print 3
    if 'predict' in train_or_predict:
        predict()

    #
    # assert model_name is not None
    # assert train_or_predict is not None
    #
    # model_file_name = model_name + '.pkl'
    # print train_or_predict
    # standard_scaler = preprocessing.StandardScaler()
    # if 'train' in train_or_predict:
    #
    #     ############################
    #     training_set = pd.read_csv(train_file_name, names=COLUMNS,
    #                                skipinitialspace=True, skiprows=1)
    #     training_label_set = deepcopy(training_set[LABEL])
    #     del training_set[LABEL]
    #
    #     training_set_imputed = deepcopy(training_set)
    #     training_set_imputed = training_set_imputed.drop(
    #         ['marital', 'job', 'contact'], axis=1)
    #     training_set_imputed['education'] = ternary_vectorizing(
    #         training_set_imputed['education'],
    #         ['primary', 'secondary', 'tertiary'])
    #     training_set_imputed['education'].replace('unknown', np.nan,
    #                                               inplace=True)
    #     training_set_imputed.fillna(training_set_imputed.mean(), inplace=True)
    #     training_set_imputed = one_hot(training_set_imputed,
    #                                    CATEGORICAL_COLUMNS_2)
    #     #
    #     training_label_set = binary_vectorizing(training_label_set,
    #                                             ['no', 'yes'])
    #     #
    #     training_set_sc_scaled_imputed = standard_scaler.fit_transform(
    #         training_set_imputed)
    #     training_set_sc_scaled_imputed = pd.DataFrame(
    #         training_set_sc_scaled_imputed)
    #
    #     fit_model = MODELS[model_name].fit(training_set_sc_scaled_imputed,
    #                                        training_label_set)
    #
    #     joblib.dump(fit_model, model_file_name)
    #     if 'predict' not in train_or_predict and 'validate' not in train_or_predict:
    #         print model_name, model_file_name
    #         return model_name, model_file_name
    #
    # print 234
    # if 'validate' in train_or_predict:
    #     print 123
    #     fit_model = joblib.load(model_file_name)
    #
    #     validation_set = pd.read_csv(validate_file_name, names=COLUMNS,
    #                                  skipinitialspace=True, skiprows=1)
    #     validation_label_set = deepcopy(validation_set[LABEL])
    #     del validation_set[LABEL]
    #
    #     #
    #     validation_set_imputed = deepcopy(validation_set)
    #     validation_set_imputed = validation_set_imputed.drop(
    #         ['marital', 'job', 'contact'], axis=1)
    #     validation_set_imputed['education'] = ternary_vectorizing(
    #         validation_set_imputed['education'],
    #         ['primary', 'secondary', 'tertiary'])
    #     validation_set_imputed['education'].replace('unknown', np.nan,
    #                                                 inplace=True)
    #     validation_set_imputed.fillna(validation_set_imputed.mean(),
    #                                   inplace=True)
    #     validation_set_imputed = one_hot(validation_set_imputed,
    #                                      CATEGORICAL_COLUMNS_2)
    #     #
    #     validation_label_set = binary_vectorizing(validation_label_set,
    #                                               ['no', 'yes'])
    #     #
    #     validation_set_sc_scaled_imputed = standard_scaler.fit_transform(
    #         validation_set_imputed)
    #     validation_set_sc_scaled_imputed = pd.DataFrame(
    #         validation_set_sc_scaled_imputed)
    #     print 'validation_set_sc_scaled_imputed'
    #     print validation_set_sc_scaled_imputed
    #     label_pred = fit_model.predict(validation_set_sc_scaled_imputed)
    #
    #     cnf_matrix = confusion_matrix(validation_label_set, label_pred)
    #     np.set_printoptions(precision=2)
    #     print model_name, cnf_matrix
    #     if 'predict' not in train_or_predict:
    #         return model_name, cnf_matrix
    #
    # if 'predict' in train_or_predict:
    #     print 123
    #     fit_model = joblib.load(model_file_name)
    #
    #     predict_set = pd.read_csv(predict_file_name, names=COLUMNS,
    #                               skipinitialspace=True, skiprows=1)
    #     validation_label_set = deepcopy(predict_set[LABEL])
    #     del predict_set[LABEL]
    #
    #     #
    #     predict_set_imputed = deepcopy(predict_set)
    #     predict_set_imputed = predict_set_imputed.drop(
    #         ['marital', 'job', 'contact'], axis=1)
    #     predict_set_imputed['education'] = ternary_vectorizing(
    #         predict_set_imputed['education'],
    #         ['primary', 'secondary', 'tertiary'])
    #     predict_set_imputed['education'].replace('unknown', np.nan,
    #                                              inplace=True)
    #     predict_set_imputed.fillna(predict_set_imputed.mean(),
    #                                inplace=True)
    #     predict_set_imputed = one_hot(predict_set_imputed,
    #                                   CATEGORICAL_COLUMNS_2)
    #     #
    #     # validation_label_set = binary_vectorizing(validation_label_set,
    #     #                                           ['no', 'yes'])
    #     #
    #     predict_set_sc_scaled_imputed = standard_scaler.fit_transform(
    #         predict_set_imputed)
    #     predict_set_sc_scaled_imputed = pd.DataFrame(
    #         predict_set_sc_scaled_imputed)
    #
    #     print 'predict_set_sc_scaled_imputed'
    #     print predict_set_sc_scaled_imputed
    #     label_pred = fit_model.predict(predict_set_sc_scaled_imputed)
    #     i = 0
    #     label_pred = ['result'] + label_pred.tolist()
    #     with open(predict_file_name, 'r') as csvinput:
    #         with open('result_'+predict_file_name, 'w') as csvoutput:
    #             writer = csv.writer(csvoutput)
    #             for row in csv.reader(csvinput):
    #                 writer.writerow(row + [str(label_pred[i])])
    #                 i += 1
    #
    #     return model_name, 'result_'+predict_file_name


def main():
    parser = OptionParser()
    parser.add_option('--model-name', dest='model_name', type="str")
    parser.add_option('--tp', dest='tp', action="append", type="str")

    (options, args) = parser.parse_args()
    run_model(options.model_name, options.tp)


if __name__ == '__main__':
    main()
