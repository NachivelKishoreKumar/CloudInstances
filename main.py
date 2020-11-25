import boto3
import argparse
import os
import time
import pprint
import json
import googleapiclient.discovery
from six.moves import input
from flask import *

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('front.html')

#select an account
@app.route('/account', methods=['POST'])
def account():
    acc = request.form['account']
    if acc == 'AWS-CLOUD':
        return render_template('aws_ins.html')
    if acc == 'GOOGLE-CLOUD':
       return render_template('compute.html')
    if acc=='AZURE':
        #return redirect(url_for('/account/azure'))
        return render_template('trial.html')
    else:
        return "select a account!...."

#list google account instance
@app.route('/account/gcloud-details', methods=['POST'])
def gcloud():
    compute = googleapiclient.discovery.build('compute', 'v1')
    project = request.form['pname']
    zone = request.form['pzone']
    result = compute.instances().list(project=project, zone=zone).execute()
    return render_template('success.html', na=result, len=len(result['items']), pro=project, zo=zone)


#List AWS instance
@app.route('/account/aws-details', methods=['POST'])
def id():
    arr = []
    idd = request.form['id']
    kkey = request.form['key']
    path = 'C:\\Users\\KUMAR\.aws\\credentials'
    fp = open(path, "w+")
    fp.write("[default]")
    fp.write('\n')
    fp.write('aws_access_key_id = ' + idd)
    fp.write('\n')
    fp.write('aws_secret_access_key = ' + kkey)
    fp.close()

    ec2client = boto3.client('ec2')
    response = ec2client.describe_instances()
    g = len(response['Reservations'])
    arr = response['Reservations']
    return render_template('aws_ins1.html', na=arr, len=len(arr), id=idd, key=kkey)
    #return response['Reservations'][0]['Instances'][0]['NetworkInterfaces'][0]['Groups'][0]


#List Azure instances
@app.route('/account/azure',methods=["post"])
def azure():
    myCmd = os.popen('az vm list').read()
    fp = open('new5.txt', 'w+')
    fp.write(myCmd)
    fp.close()
    with open('new5.txt', 'rb+') as filehandle:
        filehandle.seek(-4, os.SEEK_END)
        filehandle.truncate()
    filehandle.close()
    fp = open('new5.txt')
    data = json.load(fp)
    b=len(data)
    return render_template('try.html', a=data, len=b)
if __name__ == '__main__':
    app.run(debug=True)
