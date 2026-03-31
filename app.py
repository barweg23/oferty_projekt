import os
from flask import Flask, send_file
from flask import render_template, request, session, jsonify, url_for, redirect, flash
import random
from lib.forms import AdditionalExpanses
from lib.inventory_manager import InventoryManager
from lib.models import Inventory, Product
from lib.pdf_generator import PDFGenerator


from lib.static import SessionKeys


app = Flask(__name__)
app.secret_key = "tajny_secret_key"



@app.route('/products', methods=["POST", "GET"])
def products():
    form = AdditionalExpanses(request.form)
    if "cart" not in session.keys():
        session[SessionKeys.CART.value] = []
    if request.method == 'POST' and form.validate():
        koszty_dodatkowe = form.koszty_dodatkowe.data
        cena = form.cena.data
        session[koszty_dodatkowe] = cena
        product = Product(id=random.randint(99999, 999999), name=koszty_dodatkowe, price=cena, color=None, moc=None)
        session[SessionKeys.CART.value].append(product)
        return redirect(url_for('products'))
    inventory = Inventory([])
    inventory_manager = InventoryManager(inventory)
    inventory_manager.read_product_data()
    cart_list = []
    for product in session[SessionKeys.CART.value]:
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
    session[SessionKeys.CART.value].append(product)
    session.modified = True
    return jsonify({"cart": session[SessionKeys.CART.value]})


@app.route('/clear_cart', methods=["GET", "POST"])
def clear_cart():
    session[SessionKeys.CART.value] = []
    session.modified = True

    return redirect(url_for("products"))


@app.route('/remove_from_cart', methods=["GET", "POST"])
def remove_from_cart():
    r = request.json
    product_id = r.get('product_id')
    for product in session[SessionKeys.CART.value]:
        if product['id'] == product_id:
            session[SessionKeys.CART.value].remove(product)

    session.modified = True
    return jsonify({"cart": session[SessionKeys.CART.value]})


@app.route("/custom_cart", methods=["POST", "GET"])
def custom_cart():
    custom_dict = {}
    custom_dict["name"] = request.form.get("additional_position")
    custom_dict["price"] = request.form.get("price")
    random_id = random.randint(9999, 99999)
    custom_product = Product(id=random_id, name=custom_dict["name"], price=custom_dict["price"], color=None, moc=None)
    session[SessionKeys.CART.value].append(custom_product)

    session.modified = True

    return redirect(url_for("products"))


@app.route("/generate_pdf", methods=["POST", "GET"])
def generate_pdf():
    file_name = request.form.get("file_name")
    inventory = Inventory([])
    pdf = PDFGenerator(file_name)
    products = session[SessionKeys.CART.value]
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

