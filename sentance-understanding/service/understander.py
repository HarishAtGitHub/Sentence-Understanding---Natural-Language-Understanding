from flask import Flask, jsonify
from flask import request
from flask import abort

app = Flask(__name__)

@app.route('/ml/api/v1.0/answer', methods=['GET'])
def get_status():
    return "Hello ! Answer service is Up. Do a POST request to same URL with body in the  json form {'text':'<text>'}"

@app.route('/ml/api/v1.0/answer', methods=['POST'])
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

if __name__ == '__main__':
    app.run(debug=True)