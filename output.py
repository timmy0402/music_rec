from flask import request, Flask
import requests

#setting flask framework
app = Flask(__name__)

@app.route('/',methods=['GET', 'POST'])
def setUp():
    return render_template('index.html') 

@app.route('/process',methods=['POST'])
def process():
    return "hello"

if (__name__ == "__main__"):
    app.run()