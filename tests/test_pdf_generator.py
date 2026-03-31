from lib.inventory_manager import InventoryManager
from lib.models import Inventory
from lib.pdf_generator import PDFGenerator



if __name__ == "__main__":
    inventory = Inventory([])
    inventory_manager = InventoryManager(inventory)
    inventory_manager.read_product_data()
    print(inventory_manager.inventory.products_dict_from_id_to_name[10])

    pdf = PDFGenerator('test44')
    ids = [10, 12, 15, 20, 25]
    cart_inventory = inventory_manager.inventory.filter_by_ids(ids)
    print(cart_inventory)
    assert isinstance(cart_inventory, Inventory)
    assert len(cart_inventory.products) == 5

    pdf.generate_pdf_for_product(cart_inventory)

    # pdf.generate_pdf_for_product_form_json(json_data)
