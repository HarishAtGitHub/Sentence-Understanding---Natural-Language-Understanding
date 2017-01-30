from flask import Flask, jsonify
from flask import request
from flask import abort

app = Flask(__name__)

API_PATH = '/ml/api/'
API_VERSION = 'v1.0'

@app.route(API_PATH + API_VERSION + '/answer', methods=['GET'])
def get_status():
    return "Hello ! Answer service is Up. Do a POST request to same URL with body in the  json form {'text':'<text>'}"

@app.route(API_PATH + API_VERSION + '/answer', methods=['POST'])
def get_answer():
    try:
        text = request.json['text']
        return jsonify(process(text))
    except KeyError as ke:
        abort(417)

def process(text):
    from core.generic import generic_question
    result = generic_question.understand(text)
    return result

@app.route('/')
def root():
  return app.send_static_file('index.html')

@app.route('/<path:path>')
def static_proxy(path):
  # send_static_file will guess the correct MIME type
  return app.send_static_file(path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)