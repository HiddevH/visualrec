# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 11:29:13 2018
@author: Hidde, Maurice
"""
# Face Recognition with Flask, wohoo!
# Thanks for the example @ Aegitgey https://github.com/ageitgey/

from flask import Flask, jsonify, request, redirect, render_template, url_for
from face_compare import face_recog

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'} # Alleen plaatjes mogen gebruikt worden

app = Flask(__name__)

def allowed_file(filename): # Check of file-extension toegestaan is
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

cast_folder = 'How_i_met_your_mother' # Zo kunnen we het later dynamisch maken

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/upload/', methods=['GET', 'POST'])
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
            name = face_recog(file, cast_folder)
            #return redirect(url_for('browse'))
            return render_template('result.html', cast_folder=cast_folder, name=name)

    # Als het bestand niet geldig was, of als er nog geen file is geüpload:
    return  render_template('upload.html')

@app.route('/browse')
def browse():
    return render_template('browse.html')

#face_distances = face_recognition.face_distance(face_values, unknown_encoding) # Bereken de afstand tussen de gezichten van de cast en het onbekende img
#best_match = np.argmin(face_distances) # Zoek de image met de minste afstand tot de onbekende image
#match_file = list(known_image_encodings.keys())[best_match] # geef de image file terug die het meest lijkt op de onbekende
#name = re.sub('(^[^\\\]*[^_])', '', match_file)
#name = re.sub('\.jpeg$', '', name) # Haalt de namen uit de bestandsnamen

#return_img = match_file # Returns filename van matched image - Python display: Image(filename=match_file)

@app.route('/about_us')
def about_us():
    return render_template('about_us.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
