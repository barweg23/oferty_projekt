from dataclasses import dataclass
from typing import List
from typing import Self


@dataclass
class Product:
    id: int
    name: str
    price: int
    color: str | None
    moc: float | None

    def __eq__(self, other):
        if self.id == other:
            return True
        return False


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

    @property
    def products_dict_from_id_to_name(self):
        empty_dict = {}
        for product in self.products:
            empty_dict[product.id] = product.name
        return empty_dict

    @property
    def products_dict_from_id_to_product(self):
        empty_dict = {}
        for product in self.products:
            empty_dict[product.id] = product
        return empty_dict

    def get_product_from_product_id(self, product_id: int) -> Product:
        for product in self.products:
            if product == product_id:
                return product

    def filter_by_ids(self, ids: List[int]) -> Self:
        list_with_ids = []
        for id in ids:
            product = self.get_product_from_product_id(id)
            list_with_ids.append(product)
        return Inventory(list_with_ids)