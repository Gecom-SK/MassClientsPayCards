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

def readPDFs(prefix = "faktury/*.pdf"):
    clients = []
    for pdfFile in glob.glob(prefix):
        doc = fitz.open(pdfFile)
        # QR code
        qr = getQRcode(doc, pdfFile)
        # K úhrade
        amount = getData(doc, "K úhrade\n").split(" ")
        amount = amount[0]
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
    pdfmetrics.registerFont(TTFont('AbhayaLibre-Regular', 'fonts/AbhayaLibre-Regular.ttf')) # imports text font that can handle all the Slovak letters
    pdfmetrics.registerFont(TTFont('AbhayaLibre-Bold', 'fonts/AbhayaLibre-Bold.ttf'))
    clients = readPDFs()    # Process all the file with prefix. Default is 'faktury/*.pdf'
    # index = 0   # Name of the output PDF file
    line_margin = 0.7 # distance between the text lines on a card
    c = canvas.Canvas("Output-addresses.pdf", pagesize=A4)
    while(len(clients) > 0):
        line = 0
        for y in range(1, 31, 12):   # y coordinate of the card as a block on a A4 paper(in cm)  (0, 30, 6) will maked 5 rows instead of 6
            y += .3
            try:
                client = clients.pop()  # Pops out the client details if are no Cients left just passes
                c.setFont("AbhayaLibre-Bold", 12)
                for addr_line in client.address:
                    c.drawString(10 * cm, (y+3.5-line) * cm, addr_line)
                    line = line + line_margin
            except:
                pass
        c.showPage()
    c.save()



if(__name__ == "__main__"):
    main()