from cloudant import Cloudant
from flask import Flask, render_template, request, jsonify, redirect, url_for, send_file
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey
from cloudant.query import Query
from cloudant.index import Index
from cloudant.document import Document
import atexit
import cf_deployment_tracker
import os
import json
from werkzeug.utils import secure_filename
import csv
import sys
import datetime

from dataAnalysis.final_model_performance_measure import run_model
from dataAnalysis.final_model_performance_measure import getexistingmodeljsonfile
from dataAnalysis.final_model_performance_measure import view_saved_model

# Emit Bluemix deployment event
cf_deployment_tracker.track()

app = Flask(__name__)

db_name = 'mydb'
client = None
db = None

if 'VCAP_SERVICES' in os.environ:
    vcap = json.loads(os.getenv('VCAP_SERVICES'))
    print('Found VCAP_SERVICES')
    if 'cloudantNoSQLDB' in vcap:
        creds = vcap['cloudantNoSQLDB'][0]['credentials']
        user = creds['username']
        password = creds['password']
        url = 'https://' + creds['host']
        client = Cloudant(user, password, url=url, connect=True)
        db = client.create_database(db_name, throw_on_exists=False)
elif os.path.isfile('vcap-local.json'):
    with open('vcap-local.json') as f:
        vcap = json.load(f)
        print('Found local VCAP_SERVICES')
        creds = vcap['services']['cloudantNoSQLDB'][0]['credentials']
        user = creds['username']
        password = creds['password']
        url = 'https://' + creds['host']
        client = Cloudant(user, password, url=url, connect=True)
        db = client.create_database(db_name, throw_on_exists=False)

# On Bluemix, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
port = int(os.getenv('PORT', 8000))


def isFile(object):
    try:
        os.listdir(object)  # tries to get the objects inside of this object
        return False  # if it worked, it's a folder
    except Exception:  # if not, it's a file
        return True


def findfiles(directory):
    objects = os.listdir(directory)  # find all objects in a dir

    files = []
    for i in objects:  # check if very object in the folder ...
        if isFile(directory + i):  # ... is a file.
            files.append(i)  # if yes, append it.
    return files


def findfilesfromdb(username):
    return map(str, db[username].get_attachment())


def get_data_from_db(key, filename):
    return db[key].get_attachment(filename)


@app.route('/')
def home():
    return render_template('index.html')

# /* Endpoint to greet and add a new visitor to database.
# * Send a POST request to localhost:8000/api/visitors with body
# * {
# *     "name": "Bob"
# * }
# */


@app.route('/api/visitors', methods=['GET'])
def get_visitor():
    if client:
        return jsonify(list(map(lambda doc: doc['name'], db)))
    else:
        print('No database')
        return jsonify([])

@app.route('/api/visitors', methods=['POST'])
def put_visitor():
    user = request.json['name']
    if client:
        data = {'name': user}
        db.create_document(data)
        return 'Hello %s! I added you to the database.' % user
    else:
        print('No database')
        return 'Hello %s!' % user


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['csv'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/uploadTrain', methods=['POST'])
def upload_file_train():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'test' not in request.files:
            # flash('No file part')
            return "no file part"
        file = request.files['test']
        username = request.args.get('username')
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            # flash('No selected file')
            return "no selected file"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            trainFileName = os.path.join(filename)
            file.save(trainFileName)
            print trainFileName

            print 123
            with open(trainFileName, 'rb') as f:
                reader = csv.reader(f)
                # lis=[line.split() for line in f]
                #save to db

                from base64 import b64encode

                uploaded_file_content = b64encode(f.read())
                print 1234, trainFileName
                # data = {'file_name': trainFileName}
                if db[username].exists():
                    db[username].put_attachment(attachment=trainFileName, data=uploaded_file_content)
                else:
                    data = {'_id': username, '_attachments': {
                        trainFileName: {'data': uploaded_file_content}}}
                    db.create_document(data)

            return trainFileName
    return ''

@app.route('/train', methods=['POST'])
def train():
    model = request.json['model']
    mode = request.json['mode']
    username = request.json['username']
    fullfilename = request.json['filename']
    columns = request.json['columns']
    if columns is None:
        columns = []
    #fullfilename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    print fullfilename
    file_content = get_data_from_db(username, fullfilename)
    result = run_model(model, mode, fullfilename, username, selected_columns=columns, file_content=file_content)
    return jsonify(result)


# @app.route('/uploadedFiles', methods=['GET'])
# def uploadedFiles():
#     return jsonify(findfiles(app.config['UPLOAD_FOLDER']))


@app.route('/uploadedFilesWithDetails', methods=['GET'])
def uploadedFilesWithDetails():
    username = request.args.get('username')
    files = findfilesfromdb(username) #findfiles(app.config['UPLOAD_FOLDER'])
    result = []
    for file in files:
        fullfilename = file #os.path.join(app.config['UPLOAD_FOLDER'], file)
        if os.path.isfile(fullfilename):
            info = os.stat(fullfilename)
            with open(fullfilename, 'rb') as f:
                lis = [line.split() for line in f]
            result.append({
                'size': info.st_size,
                'lines': len(lis),
                'fields': lis[0],
                'filename': file,
                'createdAt': datetime.datetime.fromtimestamp(
                    int(info.st_ctime)
                ).strftime('%Y-%m-%d %H:%M:%S')
            })
    return jsonify(result)


def dumpCsvToJson(filename):
    with open(filename, 'rb') as f:
        reader = csv.DictReader(f)
        out = json.dumps([row for row in reader])
        return out


@app.route('/loadDistributionData', methods=['GET'])
def loadDistributionData():
    filename = request.args.get('filename')
    fullfilename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.isfile(fullfilename):
        return dumpCsvToJson(fullfilename)
    elif os.path.isfile(filename):
        return dumpCsvToJson(filename)


# @app.route('/getFiledetails', methods=['GET'])
# def getFiledetails():
#     filename = request.args.get('filename')
#     fullfilename = os.path.join(filename)
#     info = os.stat(fullfilename)
#     with open(fullfilename, 'rb') as f:
#         lis = [line.split() for line in f]
#     return jsonify({
#         'size': info.st_size,
#         'lines': len(lis),
#         'fields': lis[0]
#     })


@app.route('/getexistingmodels', methods=['GET'])
def getexistingmodels():
    result = getexistingmodeljsonfile(username=request.json['username'])
    return jsonify(result)


@app.route('/getSavedModel', methods=['POST'])
def getSavedModel():
    model = request.json['model']
    columns = request.json['columns']
    # model = model[:-4]
    result = view_saved_model(model, columns)
    return jsonify(result)

@app.route('/register', methods=['POST'])
def register():
    username = request.json['username']
    password = request.json['password']

    if Document(db, 'usercontrol').exists():
        db['usercontrol'][username] = password
        print 'update', username
    else:
        db.create_document({'_id': 'usercontrol', username: password})
        print 'create', username
    return ''

@app.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']

    if username in db['usercontrol']:
        if db['usercontrol'][username] == password:
            return ''

    return render_template('404.html'), 404

@app.route('/getFileData', methods=['GET'])
def getFileData():
    filename = request.args.get('filename')
    fullfilename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.isfile(fullfilename):
        return dumpFileData(fullfilename)
    elif os.path.isfile(filename):
        return dumpFileData(filename)

def dumpFileData(filename):
    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            break
    return jsonify({'columns': row, 'data': dumpCsvToJson(filename)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
