
from flask import Flask,render_template
from flask import jsonify
from flask import request
from main import main

app = Flask(__name__)


@app.route('/adhaar_ocr', methods=['POST'])
def addOne():
    request_ = request.get_json()
    file = request_['data']
    result = main(file)
    print(request_)
    return jsonify({'adhaar_ocr': result})


if __name__ == "__main__":
    app.run(debug=True)

