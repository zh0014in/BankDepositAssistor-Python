rt = 'bank-full.csv'
nrt = 'bank-full_new.csv'
fi = open(rt, 'r')
fo = open(nrt, 'w+')

for line in fi.readlines():
    line = line.replace('\"\";\"\"', ',')
    line = line.replace(';\"\"', ',')
    line = line.replace('\"\";', ',')
    line = line.replace(';', ',')
    line = line.replace('\"\"\"', '')
    line = line.replace('\"', '')
    fo.writelines(line)

fi.close()
fo.close()
