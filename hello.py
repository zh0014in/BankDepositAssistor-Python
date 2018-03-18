from cloudant import Cloudant
from flask import Flask, render_template, request, jsonify, redirect, url_for
import atexit
import cf_deployment_tracker
import os
import json
from werkzeug.utils import secure_filename
import csv
import sys

from dataAnalysis.final_model_performance_measure import run_model

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

# /**
#  * Endpoint to get a JSON array of all the visitors in the database
#  * REST API example:
#  * <code>
#  * GET http://localhost:8000/api/visitors
#  * </code>
#  *
#  * Response:
#  * [ "Bob", "Jane" ]
#  * @return An array of all the visitor names
#  */


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


@app.route('/upload', methods=['POST'])
def upload_file_train():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'test' not in request.files:
            # flash('No file part')
            return "no file part"
        file = request.files['test']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            # flash('No selected file')
            return "no selected file"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            trainFileName = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(trainFileName)
            print trainFileName
            return trainFileName

            # with open(fullfilename, 'rb') as f:
            #     reader = csv.reader(f)
            #     lis=[line.split() for line in f]
            #     #save to db
            #     # for row in reader:
            #         # data = {'train': row}
            #         # db.create_document(data)
            #
            #     return jsonify(lis)
    return ''


@app.route('/uploadTrain', methods=['POST'])
def upload_file_test():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'test' not in request.files:
            # flash('No file part')
            return "no file part"
        file = request.files['test']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            # flash('No selected file')
            return "no selected file"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            fullfilename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(fullfilename)

            with open(fullfilename, 'rb') as f:
                reader = csv.reader(f)
                lis = [line.split() for line in f]
                # save to db
                # for row in reader:
                # data = {'train': row}
                # db.create_document(data)

                return jsonify(lis)
    return ''


@app.route('/train', methods=['POST'])
def train():
    model = request.json['model']
    trainFileName = request.json['trainFileName']
    result = run_model(trainFileName, [model])
    return jsonify(result[model].tolist())

@atexit.register
def shutdown():
    if client:
        client.disconnect()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
