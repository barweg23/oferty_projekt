from flask import Flask
from flask import render_template, request, session, jsonify, url_for, redirect,flash
import random
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length

from main import InventoryManager, Inventory, PDFGenerator, Product

from wtforms import Form, BooleanField, StringField, PasswordField, validators

class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])

class AdditionalExpanses(Form):
    koszty_dodatkowe = StringField('koszty_dodatkowe', [validators.Length(min=4, max=50)])
    cena = IntegerField('cena', [validators.Length(min=1, max=6)])


app = Flask(__name__)
app.secret_key = "tajny_secret_key"

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        print(form.username.data, form.email.data,
                    form.password.data)
        flash('Thanks for registering')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/test")
def test_route():
    #
    return "<p>Hello, Test!!</p>"



@app.route('/clean_cart_fully/')
def clean_cart_fully():
    session['cart'] = []
    return "<p>Hello, Test!!</p>"

@app.route('/products/', methods=["GET"])
def products():
    form = AdditionalExpanses(request.form)
    print(session.keys())
    if "cart" not in session.keys():
       session['cart'] = []
    if "custom_cart" not in session.keys(): # keys values items
       session['custom_cart'] = []
    #print('custom_cart:',session['custom_cart'])
    inventory = Inventory([])
    inventory_manager = InventoryManager(inventory)
    inventory_manager.read_product_data()
    cart_list = []
    print(session['cart'])
    for product in session['cart']:
        product = inventory_manager.inventory.products_dict_from_id_to_product.get(product['id'], product)
        if product:
            cart_list.append(product)
    print(cart_list)
    print(cart_list)
    #cart_list.append('test custom query')
    return render_template('products.html', products=inventory_manager.inventory.products, products_in_cart=cart_list, form=form)

@app.route('/add_to_cart', methods=["GET","POST"])
def add_to_cart():
    r = request.json
    product_id = r.get('product_id')
    inventory = Inventory([])
    inventory_manager = InventoryManager(inventory)
    inventory_manager.read_product_data()
    product = inventory_manager.inventory.products_dict_from_id_to_product.get(product_id, None)
    print(product)
    if product:
        session['cart'].append(product)
    session.modified = True
    return jsonify({"cart": session['cart']})

@app.route('/clear_cart', methods=["GET","POST"])
def clear_cart():
    session['cart'] = []
    session.modified = True

    return redirect(url_for("products"))

@app.route('/remove_from_cart', methods=["GET","POST"])
def remove_from_cart():
    r = request.json
    product_id = r.get('product_id')
    # jesli id z sesji
    # petla po session['cart']
    #
    print(session['cart'][0]) # object -> id
    for product in session['cart']:
        if product['id'] == product_id:
            session['cart'].remove(product)

    print(product_id)
    # js do not adding number to the rendered funcion arg
    # python do not adding li with specyfic id
    session.modified = True
    return jsonify({"cart": session['cart']})

@app.route('/cart_json', methods=["GET"])
def cart_json():
    if "cart" not in session.keys():
        session['cart'] = []
    inventory = Inventory([])
    inventory_manager = InventoryManager(inventory)
    inventory_manager.read_product_data()
    products = []

    print(session['cart'])
    for _id in session['cart']:
        product = inventory_manager.inventory.get_product_from_product_id(_id)
        products.append(product)

    print(products)
    # utworzenie pustej listy
    # for z ids
    # id -> przszukanie w produktach i wyciagamy obiekt
    # obiekt jest przedstawiony w dict i oddany do listy
    # koniec petli
    # liste z produkatmi wrzuamy do jsonify


    return jsonify({"data": products})

@app.route('/cart_html', methods=["GET"])
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
    #
    return jsonify({"cart": cart})

@app.route("/custom_cart", methods=["POST", "GET"])
def custom_cart():
    # [] => add custom z 'transport' 300 -> [`{name: 'tranpsport', price: 300}`]
    custom_dict = {}
    custom_dict["name"] = request.form.get("additional_position")
    custom_dict["price"] = request.form.get("price")
    random_id = random.randint(9999,99999)
    custom_product = Product(id=random_id, name=custom_dict["name"], price=custom_dict["price"], color=None, moc=None)
    session['cart'].append(custom_product)

    session.modified = True


    return redirect(url_for("products"))



@app.route("/generate_pdf", methods=["POST", "GET"])
def generate_pdf():
    print(request.get_data())
    print(list(request.form.keys()))
    file_name = request.form.get("file_name")
    inventory = Inventory([])
    pdf = PDFGenerator(file_name)
    products = session['cart'] # products (dict -> Inventory([products]
    for product in products:
        inventory.products.append(
            Product(id=product['id'], name=product["name"], price=product["price"], color=product["color"], moc=product["moc"]))

    pdf.generate_pdf_for_product(inventory)
    #pdf.generate_pdf_for_product_from_dict(session['cart'])
    flash(f"PDF has been generated!, name = {file_name}.pdf", 'success')
    return redirect(url_for("products"))


# TODO new feature: custom fields
# mozna przygotowac jakos baze good but not enough
# nazwa cena _> dodaj + zapmietaj + wygeneruj
#

if __name__ == '__main__':
    app.run(debug=True, port=5050)