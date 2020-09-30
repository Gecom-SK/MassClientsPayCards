# Adapted from https://stackoverflow.com/questions/11817182/uploading-multiple-files-with-flask
# Adapted from https://buildcoding.com/upload-and-download-file-using-flask-in-python/
# Adapted from https://www.tutorialspoint.com/How-to-delete-all-files-in-a-directory-with-Python

from flask import Flask, render_template, request, make_response, redirect, send_file
import os
from pdfBillExtract import pbe, qrCards

UPLOAD_FOLDER = 'faktury/'
DOWNLOAD_FOLDER = ''

app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
def processPDFs():
    if request.method == 'POST':
        #   Delete all the previoously updated files from the directory
        for root, dirs, files in os.walk(UPLOAD_FOLDER):
            for file in files:
                os.remove(os.path.join(root, file))
        files = request.files.getlist("files[]")
        for file in files:
            if file.filename == '':
                print('no filename')
                return redirect(request.url)
            else:
                file.save(os.path.join(UPLOAD_FOLDER, file.filename))
                print("saved file successfully")
        pdfs = pbe.BillExtract()
        try:
            # Checks if the checkbox was checked for envelope formatted address print-out
            # Reads all the pdf files from directory, process them and returns the filename of the output pdf file.
            file_path = DOWNLOAD_FOLDER + qrCards.processClients(pdfs.readPDFs(), adresses=(request.form.get('address') == 'on'))
            #send file name as parameter to downlad
            return send_file(file_path, as_attachment=True, attachment_filename='QRcards.pdf')
        except:
            pass
    return render_template('pdfUpload.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')