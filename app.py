from flask import Flask
from flask import render_template

from main import InventoryManager, Inventory

app = Flask(__name__)

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

@app.route('/products/')
def products():
    inventory = Inventory([])
    inventory_manager = InventoryManager(inventory)
    inventory_manager.read_product_data()

    return render_template('products.html', products=inventory_manager.inventory.products)

if __name__ == '__main__':
    app.run(debug=True, port=5050)