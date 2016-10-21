from flask import Flask, request, render_template
import json
import requests
import socket
import time
from datetime import datetime
from pandas.io.json import json_normalize
from predict import unit1
import pandas as pd
import Mongo as mi



app = Flask(__name__)
PORT = 5353
REGISTER_URL = "http://10.8.2.152:5000/register"
DATA = []
TIMESTAMP = []
FRAUD = []

@app.route('/score', methods=['POST'])
def score():
    
    #gets the json data, makes it into a dataframe, call the predict file to get
    #the probability of fraud and fraud.
    data = json.dumps(request.json, sort_keys=True, indent=4, separators=(',', ': '))
    result = json_normalize(json.loads(data))
    pred, prob = unit1(result)
    DATA.append(data)
    TIMESTAMP.append(time.time())

    #stores the dataframe in the mongodb
    mi.store_data(table, time.time(), prob[0][1], result.iloc[:,18][0], data)

    return ""

#checks to make sure that the data is loading properly
@app.route('/check')
def check():
    line1 = "Number of data points: {0}".format(len(DATA))
    if DATA and TIMESTAMP:
        dt = datetime.fromtimestamp(TIMESTAMP[-1])
        data_time = dt.strftime('%Y-%m-%d %H:%M:%S')
        line2 = "Latest datapoint received at: {0}".format(data_time)
        line3 = DATA[-1]
        output = "{0}\n\n{1}\n\n{2}".format(line1, line2, line3)
    else:
        output = line1
    return output, 200, {'Content-Type': 'text/css; charset=utf-8'}


@app.route('/table')
def table():

    #creates a html table from the mongodb instances based on the columns names
    #from the list of keys below.

    #stores each fraud (when the probability of fraud is greater than .5
    #instance into the dictionary
    
    dit = {'timestamp': [],'name': [], 'fraud_prob': []}
    keys = ['timestamp','name', 'fraud_prob']
    mong = mi.get_all_data(table)
    for doc in mong:
        if doc['fraud_prob'] > 0.5:
            for key in doc:
                if key in keys:
                    if key == 'timestamp':
                        dit[key].append(datetime.fromtimestamp(doc[key]))
                    else:
                        dit[key].append(doc[key])
    df = pd.DataFrame.from_dict(dit)
    HTML = df.to_html()
    return HTML

def register_for_ping(ip, port):
    registration_data = {'ip': ip, 'port': port}
    requests.post(REGISTER_URL, data=registration_data)


if __name__ == '__main__':
    # Register for pinging service
    ip_address = socket.gethostbyname(socket.gethostname())
    print "attempting to register %s:%d" % (ip_address, PORT)
    register_for_ping(ip_address, str(PORT))

    DB_NAME = 'fraud'
    TABLE_NAME = 'fraud'
    df, table = mi.create_mongo_instance(DB_NAME, TABLE_NAME)

    # Start Flask app
    app.run(host='0.0.0.0', port=PORT, debug=True)
