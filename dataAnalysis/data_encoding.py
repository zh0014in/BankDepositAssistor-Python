from copy import deepcopy
import pandas as pd

def one_hot(dtf, cols):
    df = deepcopy(dtf)
    for each in cols:
        dummies = pd.get_dummies(df[each], prefix=each, drop_first=False)
        df = pd.concat([df, dummies], axis=1)
    df = df.drop(cols, axis=1)
    return df

def label_vec(dtf):
    df = deepcopy(dtf)
    df.replace(to_replace=['no', 'yes'], value=[0,1], inplace=True)
    return  df

def binary_vectorizing(dtf, labels):
    df = deepcopy(dtf)
    df.replace(to_replace=labels, value=[0,1], inplace=True)
    return  df

def ternary_vectorizing(dtf, labels):
    df = deepcopy(dtf)
    df.replace(to_replace=labels, value=[1,2,3], inplace=True)
    return  df


def main():
    BANK_VALIDATION = "bank-crossvalidation_new.csv"

    COLUMNS = ["age", "job", "marital", "education", "default", "balance", "housing", "loan", "contact", "day", "month",
               "duration",
               "campaign", "pdays", "previous", "poutcome", "y"]
    CATEGORICAL_COLUMNS = ["job", "marital", "education", "default", "housing", "loan", "contact", "day", "month",
                           "poutcome"]
    LABEL = "y"

    validation_set = pd.read_csv(BANK_VALIDATION, names=COLUMNS, skipinitialspace=True, skiprows=1)
    validation_label_set = deepcopy(validation_set[LABEL])
    del validation_set['y']

    # Vectorize the categorical columns
    df = one_hot(validation_set, cols=CATEGORICAL_COLUMNS)

    #Vectorize the label column
    df_label = label_vec(validation_label_set)

    print(df.head())
    print(df_label.head())


if __name__ == '__main__':
    main()