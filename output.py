from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/run_python', methods=['POST'])
def run_python():
    return request.data

if __name__ == '__main__':
    app.run(port=5000)