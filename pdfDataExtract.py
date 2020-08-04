import fitz
import glob
import PIL


class Client:
    
    def __init__(self, qrCode, address, ammount, iban, acc, bic, vs):
        self.qrCode = qrCode
        self.address = address
        self.ammount = ammount
        self.iban = iban
        self.acc = acc
        self.bic = bic
        self.vs = vs

    def __str__(self):
        return f'QRcode: {self.qrCode}\nAdresa: {self.address}\nIBAN: {self.iban}\nUcet: {self.acc}\nBIC: {self.bic}\nVS: {self.vs}\nSuma: {self.ammount}'

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
        all_texts = page.getText()
        key_locator = all_texts.find(key) + len(key)
        value_end = all_texts.find('\n', key_locator)
        data = all_texts[key_locator:value_end]
        return data.strip()

def getDataLines(doc, key, lines=1):
    for page in doc:
        text_lines = page.getText().strip().split("\n")
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
        ammount = getData(doc, "K úhrade\n")
        # address
        addr = "\n".join(getDataLines(doc, "Slovensko", 3))
        # IBAN & Ucet
        acc = getDataLines(doc, "Účet:", 2)
        iban = acc[0]
        ucet = acc[1]
        # BIC
        bic = getData(doc, "BIC: ")
        # Variabilny symbol
        vs = getData(doc, "VS: ")
        clients.append(Client(qr, addr, ammount, iban, ucet, bic, vs))
    return clients

def main():
    clients = readPDFs()
    for client in clients:
        print(client, end='\n\n')


if(__name__ == "__main__"):
    main()