from this import d
from flask import Flask,jsonify

a=10
b=100
c=90
appFlask = Flask(__name__)
@appFlask.route('/')
def add():
    d=10+2+1
    
    return jsonify(d)
if __name__=='__main__':
    appFlask.run(debug=True)
