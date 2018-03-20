from copy import deepcopy
import pandas as pd
from data_encoding import one_hot, binary_vectorizing, ternary_vectorizing
from sklearn import svm, preprocessing
from sklearn.metrics import confusion_matrix
import sklearn.linear_model as lm
import numpy as np
import csv
from sklearn.ensemble import RandomForestClassifier

from optparse import OptionParser
from sklearn.externals import joblib

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
    'rf': RandomForestClassifier(max_depth=3, random_state=1),
    'lm': lm.LogisticRegression(),
    'svm': svm.SVC(kernel='rbf', degree=16, max_iter=100)
}


def run_model(model_name, train_or_predict, file_name):
    def train():
        training_set = pd.read_csv(file_name, names=COLUMNS,
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
        # print fit_model.feature_importances_
        importances = []
        if (model_name == "rf"):
            importances = fit_model.feature_importances_
            feature_importance_output = "rf_feature_importance.csv"
        elif (model_name == "lm"):
            importances = fit_model.coef_[0]
            feature_importance_output = "lm_feature_importance.csv"

        if (len(importances)):
            print importances
            print len(importances)
            feature_names = training_set_imputed.keys()
            indices = np.argsort(importances)[::-1]
            df = pd.DataFrame(columns=['features', 'importance'])
            for f in range(training_set_sc_scaled_imputed.shape[1]):
                print("%d. feature %s (%f)" % (f + 1, feature_names[indices[f]], importances[indices[f]]))
                df.loc[f] = [feature_names[indices[f]], importances[indices[f]]]
            df.to_csv(feature_importance_output)

        joblib.dump(fit_model, model_file_name)

        print model_name, model_file_name
        return model_name, fit_model.get_params(), feature_importance_output

    def validate():
        fit_model = joblib.load(model_file_name)

        validation_set = pd.read_csv(file_name, names=COLUMNS,
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

        return model_name, cnf_matrix

    def predict():
        fit_model = joblib.load(model_file_name)

        predict_set = pd.read_csv(file_name, names=COLUMNS,
                                  skipinitialspace=True, skiprows=1)
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

        predict_set_sc_scaled_imputed = standard_scaler.fit_transform(
            predict_set_imputed)
        predict_set_sc_scaled_imputed = pd.DataFrame(
            predict_set_sc_scaled_imputed)

        print 'predict_set_sc_scaled_imputed', list(
            predict_set_sc_scaled_imputed.columns.values)

        label_pred = fit_model.predict(predict_set_sc_scaled_imputed)
        i = 0
        label_pred = ['y'] + label_pred.tolist()
        result = []

        with open(file_name, 'r') as csvinput:
            for row in csv.reader(csvinput):
                if i == 0:
                    result.append(COLUMNS)
                else:
                    row[-1] = 'no' if label_pred[i] == 0 else 'yes'
                    result.append(row)
                i += 1

        return model_name, result

    assert model_name is not None
    assert train_or_predict is not None

    model_file_name = model_name + '.pkl'
    print train_or_predict
    standard_scaler = preprocessing.StandardScaler()

    if 'train' == train_or_predict:
        return train()

    if 'validate' == train_or_predict:
        return validate()

    if 'predict' == train_or_predict:
        return predict()


def main():
    parser = OptionParser()
    parser.add_option('--model-name', dest='model_name', type="str")
    parser.add_option('--tp', dest='tp', type="str")
    parser.add_option('--file-name', dest='file_name', type="str")
    (options, args) = parser.parse_args()

    print run_model(options.model_name, options.tp, options.file_name)
    # train_file_name='bank-training_new.csv',
    # validate_file_name='bank-training_new.csv',
    # # predict_file_name='bank-testing_new.csv'):
    # predict_file_name='bank-predict3.csv'):


if __name__ == '__main__':
    main()
