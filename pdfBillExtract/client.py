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