from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    return ""


@app.route("/product/<int:product_id>")
def product(product_id):
    print('load productid: ' + str(product_id))
    with open('../data/products/products/de/' + str(product_id) + '.json') as f:
        return f.read()


@app.route('/customer/rating/<int:customer_id>')
def customerRating(customer_id):
    print('load customer with id: ' + str(customer_id))
    with open('../data/customers/' + str(customer_id) + '.json') as f:
        return f.read()
