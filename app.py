from flask import Flask
from flask import render_template, request, session, jsonify

from main import InventoryManager, Inventory

app = Flask(__name__)
app.secret_key = "tajny_secret_key"
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/test")
def test_route():
    #
    return "<p>Hello, Test!!</p>"



@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    print('test')
    return render_template('hello.html', person=name)

@app.route('/products/', methods=["GET"])
def products():
    inventory = Inventory([])
    inventory_manager = InventoryManager(inventory)
    inventory_manager.read_product_data()

    return render_template('products.html', products=inventory_manager.inventory.products)

@app.route('/add_to_cart', methods=["GET","POST"])
def add_to_cart():
    if "cart" not in session.keys():
       session['cart'] = []
    session['cart'].append(42)
    # read from post
    # add to session
    # display session
    session.modified = True

    return jsonify({"cart": 'cart'})

@app.route('/cart', methods=["GET"])
def cart():
    session['test'] = 'test_string'
    session['test_int'] = 'test_int'
    #session['cart'] = []
    print(session.keys())
    if "cart" not in session.keys(): # keys values items
       session['cart'] = []
    # so mark it as modified yourself
    #cart = session['cart']
    print(session)
    cart = 'temp'
    return jsonify({"cart": cart})



if __name__ == '__main__':
    app.run(debug=True, port=5050)