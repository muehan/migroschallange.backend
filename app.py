from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/product/<int:product_id>")
def product(product_id):
    print('load productid: ' + str(product_id))
    with open('../data/products/products/de/' + str(product_id) + '.json') as f:
        return f.read()