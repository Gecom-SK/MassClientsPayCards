import fitz
import glob
import PIL
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.utils import Image
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import reportlab
import pdfBillExtract
from pdfBillExtract.pbe import BillExtract, Client

def processClients(clients, out_file = 'output.pdf', adresses=False):
    if(adresses):
        envelope_clients = clients.copy()
    reportlab.rl_config.warnOnMissingFontGlyphs = 0
    pdfmetrics.registerFont(TTFont('AbhayaLibre-Regular', 'fonts/AbhayaLibre-Regular.ttf')) # imports text font that can handle all the Slovak letters
    pdfmetrics.registerFont(TTFont('AbhayaLibre-Bold', 'fonts/AbhayaLibre-Bold.ttf'))
    line_margin = 0.4 # distance between the text lines on a card
    c = canvas.Canvas(out_file, pagesize=A4)
    while(len(clients) > 0):
        c.setFont("AbhayaLibre-Bold", 8)
        count = 0
        for y in range(0, 30, 5):   # y coordinate of the card as a block on a A4 paper(in cm)  (0, 30, 6) will maked 5 rows instead of 6
            y += .3
            for x in range(0, 20, 10):  # x coordinate of the card as a block on a A4 paper(in cm) 
                x += .5
                try:
                    client = clients.pop()  # Pops out the client details if are no Cients left just passes
                    c.drawImage(client.qrCode, x * cm, (y + .2) * cm, width=3.6 * cm, height=3.6 * cm)  # draws QR code image. Please note the dimentions (3.6 by 3.6 cm)
                    # c.drawImage("Gecom znak.png", (x+4) * cm, (y + .2 - 4) * cm, width=2 * cm, height=2 * cm, mask='auto' )
                    line = 0
                    c.setFont("AbhayaLibre-Bold", 11)
                    c.drawString((x+3.7) * cm, (y+3.5-line) * cm, f'Variabilný symbol - {client.vs}')
                    line = line + line_margin
                    c.setFont("AbhayaLibre-Bold", 12)
                    c.drawString((x+3.7) * cm, (y+3.5-line) * cm, f'Suma - € {client.amount}')
                    line = line + line_margin + 0.3
                    c.setFont("AbhayaLibre-Bold", 8)
                    c.drawString((x+3.7) * cm, (y+3.5-line) * cm, f'IBAN :')
                    line = line + line_margin
                    c.drawString((x+3.7) * cm, (y+3.5-line) * cm, f'{client.iban}')
                    line += .8
                    for addr_line in client.address:
                        c.drawString((x+3.7) * cm, (y+3.5-line) * cm, addr_line)
                        line = line + line_margin
                    count += 1
                except Exception as e:
                    # print(e)
                    pass
        c.showPage()
        ## BACK-SIDE
        ##
        bk_count = 0
        c.setFont("AbhayaLibre-Bold", 8)
        for y in range(0, 30, 5):   # y coordinate of the card as a block on a A4 paper(in cm)  (0, 30, 6) will maked 5 rows instead of 6
            for x in range(13, 0, -10):  # x coordinate of the card as a block on a A4 paper(in cm) 
                try:
                    line = 1
                    if (bk_count < count):
                        c.setFont("AbhayaLibre-Bold", 14)
                        c.drawString((x+.7) * cm, (y+3.5-line) * cm, 'Pri strate - poplatok 3€')
                        line = line + line_margin
                        c.setFont("AbhayaLibre-Bold", 12)
                        c.drawString((x+.7) * cm, (y+3.5-line) * cm, 'za vystavenie novej kartičky.')
                        line = line + line_margin + 0.3
                        c.setFont("AbhayaLibre-Bold", 8)
                        c.drawString((x+.7) * cm, (y+3.5-line) * cm, 'Pri zmene programu je potrebné si vyžiadať novú kartičku.')
                        line = line + line_margin
                        c.drawString((x+.7) * cm, (y+3.5-line) * cm, 'Bez poplatku.')
                    bk_count += 1
                except Exception as e:
                    print(e)                    
        c.showPage()
    if(adresses):
        line_margin = 0.7 # distance between the text lines on a card
        # c = canvas.Canvas("Output-addresses.pdf", pagesize=A4)
        while(len(envelope_clients) > 0):
            line = 0
            for y in range(1, 31, 12):   # y coordinate of the card as a block on a A4 paper(in cm)  (0, 30, 6) will maked 5 rows instead of 6
                y += .3
                try:
                    client = envelope_clients.pop()  # Pops out the client details if are no Cients left just passes
                    c.setFont("AbhayaLibre-Bold", 12)
                    for addr_line in client.address:
                        c.drawString(10 * cm, (y+3.5-line) * cm, addr_line)
                        line = line + line_margin
                except:
                    pass
            c.showPage()
    c.save()
    return out_file
