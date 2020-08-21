import fitz
import glob
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import reportlab
from pdfBillExtract.client import Client

class BillExtract:
    
    def __init__(self, prefix='faktury/*.pdf'):
        self.prefix = prefix

    def _getQRcode(self, name):
        for i in range(len(self.doc)):
            for img in self.doc.getPageImageList(i):
                xref = img[0]
                pix = fitz.Pixmap(self.doc, xref)
                if pix.n < 5:       # this is GRAY or RGB
                    pix.writePNG(f"{name}.png")
                else:               # CMYK: convert to RGB first
                    pix1 = fitz.Pixmap(fitz.csRGB, pix)
                    pix1.writePNG(f"{name}.png")
                    pix1 = None
                pix = None
        return f"{name}.png"
        
    def _getData(self, key):
        for page in self.doc:
            all_texts = page.getText().encode('utf-8').decode('utf-8')
            key_locator = all_texts.find(key) + len(key)
            value_end = all_texts.find('\n', key_locator)
            data = all_texts[key_locator:value_end]
            return data.strip()

    def _getDataLines(self, key, lines=1):
        for page in self.doc:
            text_lines = page.getText().strip().encode('utf-8').decode('utf-8').split("\n")
            for num, line in enumerate(text_lines):
                if line == key:
                    return text_lines[(num+1):(num+lines+1)]
        return ""

    def readPDFs(self):
        clients = []
        for pdfFile in glob.glob(self.prefix):
            self.doc = fitz.open(pdfFile)
            # QR code
            qr = self._getQRcode(pdfFile)
            # K úhrade
            amount = self._getData("K úhrade\n").split(" ")
            amount = amount[0]
            # address
            addr = self._getDataLines("Slovensko", 3)
            # IBAN & Ucet
            acc = self._getDataLines("Účet:", 2)
            iban = acc[0]
            ucet = acc[1]
            # BIC
            bic = self._getData("BIC: ")
            # Variabilny symbol
            vs = self._getData("VS: ")
            clients.append(Client(qr, addr, amount, iban, ucet, bic, vs))
        return clients