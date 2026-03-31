from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from lib.models import Inventory
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

class PDFGenerator:
    def __init__(self, file_name):
        self.path = f"data/output/{file_name}.pdf"

    def generate_pdf_for_product(self, inventory: Inventory):
        pdfmetrics.registerFont(TTFont("DejaVuSans", "static/pdf/DejaVuSans.ttf"))

        doc = SimpleDocTemplate(self.path, pagesize=letter)

        styles = getSampleStyleSheet()

        table = Table(inventory.data)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("ALIGN", (1, 1), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, -1), "DejaVuSans")
        ]))

        doc.build([table])
