import csv
from lib.models import Inventory, Product


class InventoryManager:
    def __init__(self, inventory: Inventory):
        self.inventory = inventory

    def read_product_data(self):
        with open("data/dane.csv", "r", encoding="utf-8-sig") as plik:
            czytnik = csv.reader(plik, delimiter=";")
            for i in czytnik:
                p = Product(int(i[0]), i[1], int(i[2]), None, None)
                self.inventory.products.append(p)