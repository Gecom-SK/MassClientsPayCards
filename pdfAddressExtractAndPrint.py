import fitz
import glob
import PIL
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import reportlab
import pdfBillExtract
from pdfBillExtract.pbe import BillExtract

def main():
    reportlab.rl_config.warnOnMissingFontGlyphs = 0
    pdfmetrics.registerFont(TTFont('AbhayaLibre-Regular', 'fonts/AbhayaLibre-Regular.ttf')) # imports text font that can handle all the Slovak letters
    pdfmetrics.registerFont(TTFont('AbhayaLibre-Bold', 'fonts/AbhayaLibre-Bold.ttf'))
    pbe = BillExtract()
    clients = pbe.readPDFs()    # Process all the file with prefix. Default is 'faktury/*.pdf'
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