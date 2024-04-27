from flask import Flask, request, jsonify
from flask_cors import CORS
import Chatbot_demo as cd

app = Flask(__name__)
CORS(app)

@app.route('/run_python', methods=['GET','POST'])
def run_python():
    cd.chatbot(request.data)
    return request.data

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000, debug=True)