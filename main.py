#wczytanie csv ;
#jeden wiersz jedna isntacja dataclass z dwoma artybumtami, kolor, moc
# lista dataclass
# czesc, wybor z tej dataclasy moze byc wykorzysytany do generatora pdf
#

from dataclasses import dataclass
from typing import List
import csv
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

pdfmetrics.registerFont(TTFont("DejaVuSans", "static/pdf/DejaVuSans.ttf"))

@dataclass
class Product:
    id: int
    name: str
    price: int
    color: str
    moc: float

@dataclass
class Inventory:
    products: List[Product]

    def convert_to_pdf_data(self):
        data = []
        for row in self.products:
            data.append([row.name, row.price])
        return data

    @property
    def data(self):
        return self.convert_to_pdf_data()



class InventoryManager:
    def __init__(self, inventory: Inventory):
        self.inventory = inventory

    def read_product_data(self):
        with open("data/dane.csv", "r", encoding="utf-8-sig") as plik:
            czytnik = csv.reader(plik, delimiter=";")
            for i in czytnik:
                p = Product(int(i[0]), i[1], int(i[2]), None, None)
                self.inventory.products.append(p)







class PDFGenerator:
    def __init__(self, file_name):
        self.path = f"data/output/{file_name}.pdf"


    def generate_pdf_for_product(self, inventory: Inventory):
        doc = SimpleDocTemplate(self.path, pagesize=letter)

        styles = getSampleStyleSheet()

        table = Table(inventory.data)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("ALIGN", (1, 1), (-1, -1), "CENTER"),
            ("FONTNAME", (0,0), (-1,-1), "DejaVuSans")
        ]))

        doc.build([table])


if __name__ == "__main__":
    inventory = Inventory([])
    inventory_manager = InventoryManager(inventory)
    inventory_manager.read_product_data()
    print(inventory_manager.inventory)
    #pdf = PDFGenerator('test2')
    #pdf.generate_pdf_for_product(inventory_manager.inventory)