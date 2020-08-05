import fitz
import glob
import PIL
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import reportlab


class Client:
    
    def __init__(self, qrCode, address, amount, iban, acc, bic, vs):
        self.qrCode = qrCode
        self.address = address
        self.amount = amount
        self.iban = iban
        self.acc = acc
        self.bic = bic
        self.vs = vs

    def __str__(self):
        return f'QRcode: {self.qrCode}\nAdresa: {self.address}\nIBAN: {self.iban}\nUcet: {self.acc}\nBIC: {self.bic}\nVS: {self.vs}\nSuma: {self.amount}'

def getQRcode(doc, name):
    for i in range(len(doc)):
        for img in doc.getPageImageList(i):
            xref = img[0]
            pix = fitz.Pixmap(doc, xref)
            if pix.n < 5:       # this is GRAY or RGB
                pix.writePNG(f"{name}.png")
            else:               # CMYK: convert to RGB first
                pix1 = fitz.Pixmap(fitz.csRGB, pix)
                pix1.writePNG(f"{name}.png")
                pix1 = None
            pix = None
    return f'{name}.png'
    
def getData(doc, key):
    for page in doc:
        all_texts = page.getText().encode('utf-8').decode('utf-8')
        key_locator = all_texts.find(key) + len(key)
        value_end = all_texts.find('\n', key_locator)
        data = all_texts[key_locator:value_end]
        return data.strip()

def getDataLines(doc, key, lines=1):
    for page in doc:
        text_lines = page.getText().strip().encode('utf-8').decode('utf-8').split("\n")
        for num, line in enumerate(text_lines):
            if line == key:
                return text_lines[(num+1):(num+lines+1)]
    return ""

def readPDFs():
    clients = []
    for pdfFile in glob.glob("faktury/*.pdf"):
        doc = fitz.open(pdfFile)
        # QR code
        qr = getQRcode(doc, pdfFile)
        # K úhrade
        amount = getData(doc, "K úhrade\n")
        # address
        addr = getDataLines(doc, "Slovensko", 3)
        # IBAN & Ucet
        acc = getDataLines(doc, "Účet:", 2)
        iban = acc[0]
        ucet = acc[1]
        # BIC
        bic = getData(doc, "BIC: ")
        # Variabilny symbol
        vs = getData(doc, "VS: ")
        clients.append(Client(qr, addr, amount, iban, ucet, bic, vs))
    return clients

def main():
    reportlab.rl_config.warnOnMissingFontGlyphs = 0
    pdfmetrics.registerFont(TTFont('AbhayaLibre-Regular', 'fonts/AbhayaLibre-Regular.ttf'))
    clients = readPDFs()
    index = 0
    while(len(clients) > 0):
        c = canvas.Canvas(f"Output-{index}.pdf", pagesize=A4)
        c.setFont("AbhayaLibre-Regular", 8)
        for y in range(0, 30, 5):
            for x in range(0, 20, 10):
                try:
                    client = clients.pop()
                    c.drawImage(client.qrCode, x * cm, y * cm, width=3.6 * cm, height=3.6 * cm)
                    i = 0
                    for line in client.address:
                        c.drawString((x+3.7) * cm, (y+3.5-i) * cm, line)
                        i = i + .5
                    c.drawString((x+3.7) * cm, (y+3.5-i) * cm, f'IBAN: {client.iban}')
                    i = i + .5
                    c.drawString((x+3.7) * cm, (y+3.5-i) * cm, f'BIC: {client.bic}')
                    i = i + .5
                    c.drawString((x+3.7) * cm, (y+3.5-i) * cm, f'Učet: {client.acc}')
                    i = i + .5
                    c.drawString((x+3.7) * cm, (y+3.5-i) * cm, f'Variabilný symbol: {client.vs}')
                    i = i + .5
                    c.drawString((x+3.7) * cm, (y+3.5-i) * cm, f'Suma: {client.amount}')
                except:
                    pass
        c.save()            



if(__name__ == "__main__"):
    main()