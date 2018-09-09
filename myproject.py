from flask import Flask
app = Flask(__name__)

@app.route('/hi/')
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"

if __name__ == "__main__":
    app.run(host='0.0.0.0')

@app.route('/bye/')
def bye():
    return "<h1 style='color:blue'>Bye!</h1>"

if __name__ == "__main__":
    app.run(host='0.0.0.0')
