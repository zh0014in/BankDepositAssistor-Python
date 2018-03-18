import csv
from random import random as rand
import sys

full = 'bank-full.csv'
cv = 'bank-crossvalidation.csv'
testing = 'bank-testing.csv'
training = 'bank-training.csv'

ff = open(full, newline='')
fcv = open(cv, 'w', newline='')
ftest = open(testing, 'w', newline='')
ftrain = open(training, 'w', newline='')

reader = csv.reader(ff)
writer_fcv = csv.writer(fcv)
writer_ftest = csv.writer(ftest)
writer_ftrain = csv.writer(ftrain)

try:
    for row in reader:
        p = rand()
        if p < 0.2:
            writer_fcv.writerow(row)
        elif p <0.4:
            writer_ftest.writerow(row)
        else:
            writer_ftrain.writerow(row)
except csv.Error as e:
    sys.exit('line {}: {}'.format(reader.line_num, e))
