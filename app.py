import os
from flask import Flask, send_file
from flask import render_template, request, session, jsonify, url_for, redirect, flash
import random
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length
from main import InventoryManager, Inventory, PDFGenerator, Product
from wtforms import Form, BooleanField, StringField, PasswordField, validators

#TODO
# forms -> to new files and import here

#TODO
# SessionManager + keys for session in class / enum -> rekomenduje enum

class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])


class AdditionalExpanses(Form):
    koszty_dodatkowe = StringField('koszty_dodatkowe', [validators.Length(min=4, max=50)])
    cena = IntegerField('cena', [validators.NumberRange(min=0, max=60000000)])


app = Flask(__name__)
app.secret_key = "tajny_secret_key"


@app.route('/products', methods=["POST", "GET"])
def products():
    form = AdditionalExpanses(request.form)
    if "cart" not in session.keys():
        session['cart'] = []
    if "custom_cart" not in session.keys():  # keys values items
        session['custom_cart'] = []
    if request.method == 'POST' and form.validate():
        koszty_dodatkowe = form.koszty_dodatkowe.data
        cena = form.cena.data
        session[koszty_dodatkowe] = cena
        product = Product(id=random.randint(99999, 999999), name=koszty_dodatkowe, price=cena, color=None, moc=None)
        session['cart'].append(product)
        return redirect(url_for('products'))
    inventory = Inventory([])
    inventory_manager = InventoryManager(inventory)
    inventory_manager.read_product_data()
    cart_list = []
    for product in session['cart']:
        product = inventory_manager.inventory.products_dict_from_id_to_product.get(product['id'], product)
        if product:
            cart_list.append(product)
    return render_template('products.html', products=inventory_manager.inventory.products, products_in_cart=cart_list,
                           form=form)


@app.route('/add_to_cart', methods=["GET", "POST"])
def add_to_cart():
    r = request.json
    product_id = r.get('product_id')
    inventory = Inventory([])
    inventory_manager = InventoryManager(inventory)
    inventory_manager.read_product_data()
    product = inventory_manager.inventory.products_dict_from_id_to_product.get(int(product_id), None)
    session['cart'].append(product)
    session.modified = True
    return jsonify({"cart": session['cart']})


@app.route('/clear_cart', methods=["GET", "POST"])
def clear_cart():
    session['cart'] = []
    session.modified = True

    return redirect(url_for("products"))


@app.route('/remove_from_cart', methods=["GET", "POST"])
def remove_from_cart():
    r = request.json
    product_id = r.get('product_id')
    for product in session['cart']:
        if product['id'] == product_id:
            session['cart'].remove(product)

    session.modified = True
    return jsonify({"cart": session['cart']})


@app.route("/custom_cart", methods=["POST", "GET"])
def custom_cart():
    custom_dict = {}
    custom_dict["name"] = request.form.get("additional_position")
    custom_dict["price"] = request.form.get("price")
    random_id = random.randint(9999, 99999)
    custom_product = Product(id=random_id, name=custom_dict["name"], price=custom_dict["price"], color=None, moc=None)
    session['cart'].append(custom_product)

    session.modified = True

    return redirect(url_for("products"))


@app.route("/generate_pdf", methods=["POST", "GET"])
def generate_pdf():
    file_name = request.form.get("file_name")
    inventory = Inventory([])
    pdf = PDFGenerator(file_name)
    products = session['cart']
    for product in products:
        inventory.products.append(
            Product(id=product['id'], name=product["name"], price=product["price"], color=product["color"],
                    moc=product["moc"]))

    pdf.generate_pdf_for_product(inventory)
    flash(f"PDF has been generated!, name = {file_name}.pdf", 'success')
    return redirect(url_for("products"))


@app.route("/api/search", methods=["POST", "GET"])
def search():
    query = request.args.get('q', '').lower()
    inventory = Inventory([])
    inventory_manager = InventoryManager(inventory)
    inventory_manager.read_product_data()
    filtered_list = []
    for product in inventory.products:  # query in name
        if query in product.name.lower():
            filtered_list.append(product)
    return jsonify(filtered_list)


@app.route("/download", methods=["GET"])
def browse_pdfs():
    pdfs_list = os.listdir('data/output/')
    return render_template('download.html', pdfs_list=pdfs_list)


@app.route("/download/<filename>")
def download_file(filename):
    return send_file(f"data/output/{filename}", as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True, port=5052)

