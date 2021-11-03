import json, time, base64
import csv
from flask import *
from io import StringIO

app = Flask(__name__)

@app.route('/')
def index():
    resp = make_response('Index generic response!')
    return resp

@app.route('/extractor/', methods=['POST'])
def extract():
    provided_keys = request.json.keys()
    for key in ["sessionId", "documentId", "provenanceId", "documentType", "dataFormat", "fileBase64"]:
        if key not in provided_keys:
            abort(400, description = f"Key {key} is missing in body!")
    sessionId       = request.json["sessionId"]
    documentId      = request.json["documentId"]
    provenanceId    = request.json["provenanceId"]
    documentType    = request.json["documentType"]
    dataFormat      = request.json["dataFormat"]
    fileBase64      = request.json["fileBase64"]

    DATA = StringIO(base64.b64decode(fileBase64).decode("utf-8"))
    table = csv.DictReader(DATA, delimiter=";")
    extract_data = []
    
    for row in table:
        extract_data.append({
            'ref': row['ref'],
            'name': row['name'],
            'value': row['value']
        })
    
    return jsonify(
        {
            "sessionId":    sessionId,
            "documentId":   documentId,
            "provenanceId": provenanceId,
            "documentType": documentType,
            "dataFormat":   dataFormat,
            "data":         extract_data
        }
    )

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=7777)