import flask
from flask import request, jsonify
from flask_cors import CORS
import json

app = flask.Flask(__name__)
app.config["DEBUG"] = True
cors = CORS(app)


@app.route('/', methods=['GET'])
def home():
    return "<h1><u>NLP based Context Analyzer</u></h1><p>This is a NLP based Context Analyzing tool. <br /> Developer(s) never take responsibility of any cases or results missed. <br /> It is just a tool proposed for helping searcher out there.</p>"


# def apply
@app.route('/analyze', methods=['POST'])
def analyze_context():
    data = request.json.get('data', "")
    input_data = request.json.get('test', "")
    new_line = data.split('\n')
    new_sentence = []
    for i in new_line:
        new_sentence.extend(i.split('.'))

    # print(new_sentence)
    return jsonify([' dataset you can cluster it (for example using KMeans from scikit learn) after obtaining the representation, and before predicting on new da'])

app.run()