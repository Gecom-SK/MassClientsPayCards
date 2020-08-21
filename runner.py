from pdfBillExtract.pbe import BillExtract
from pdfBillExtract.qrCards import processClients

processClients(BillExtract().readPDFs())







