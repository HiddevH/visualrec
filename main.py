# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 11:29:13 2018
@author: Hidde
"""

# Face Recognition with Flask, wohoo!
# Thanks for the example @ Aegitgey https://github.com/ageitgey/

from flask import Flask, jsonify, request, redirect, render_template, url_for
from flask_bootstrap import Bootstrap
from face_compare import face_recog

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'} # Alleen plaatjes mogen gebruikt worden

app = Flask(__name__)
Bootstrap(app)

def allowed_file(filename): # Check of file-extension toegestaan is
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

cast_folder = 'Game_of_Thrones' # Zo kunnen we het later dynamisch maken

@app.route('/', methods=['GET', 'POST'])

def upload_image():
    # Check if a valid image file was uploaded
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            # Image is geldig, we runnen het face_recog script en krijgen de naam + bestandsnaam van de match terug
            name, img = face_recog(file, cast_folder)
           # img = img.rsplit('\\', 1)[1]
            return render_template('result.html', img=img, name=name)

    # Als het bestand niet geldig was, of als er nog geen file is geüpload: 
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0')
