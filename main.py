# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 11:29:13 2018
@author: Hidde, Maurice
"""
# Face Recognition with Flask, wohoo!
# Thanks for the example @ Aegitgey https://github.com/ageitgey/

from flask import Flask, jsonify, request, redirect, render_template, url_for, session
from face_compare import face_recog
from browse_casts import get_browse_casts, get_cast_count
from datetime import timedelta

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'} # Alleen plaatjes mogen gebruikt worden

app = Flask(__name__)
app.config['SECRET_KEY'] = "winteriscoming"

def allowed_file(filename): # Check of file-extension toegestaan is
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#selected_cast = 'Game_of_Thrones' # Deze variabele moet eigenlijk uit browse.html komen

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
            results, error = face_recog(file)  # Returns dict met {cast : bijhorende match} en evt error message
            if len(error) > 1:  # If the error variable contains a message
                return render_template('upload.html', error=error)  # Let the user upload another photo

            session['results'] = results
            app.permanent_session_lifetime = timedelta(minutes=10)  # Bewaar de resultaten voor 10 min
            session.permanent = False  # Vernietig de session bij browser quit
            return redirect(url_for('result')) #render_template('result.html', selected_cast=selected_cast, name=results[selected_cast])
    # Als het bestand niet geldig was, of als er nog geen file is geüpload:
    return  render_template('upload.html')

@app.route('/result')
def result():
    if 'results' not in session: # Als er nog geen results dict is, laad de upload pagina
        return redirect(url_for('upload_image'))
    elif 'selected_cast' not in session:
        return redirect(url_for('browse'))

    selected_cast = session['selected_cast']
    import time
    time.sleep(1)
    return render_template('result.html', selected_cast=selected_cast, name=session['results'][selected_cast]) # Anders, toon resultaten

@app.route('/browse', methods=['GET', 'POST'])
def browse():
    if request.method == 'POST': # Check if user selected cast
        session['selected_cast'] = request.form['selected_cast']
        return redirect(url_for('result'))
    browsable_casts = get_browse_casts()  # Get a list of all browsable casts
    cast_count = get_cast_count()  # Get the dict with the amount of characers in each cast
    return render_template('browse.html', casts=browsable_casts, len=len(browsable_casts), cast_count=cast_count)

@app.route('/about_us')
def about_us():
    return render_template('about_us.html')

if __name__ == "__main__":
    app.config['SECRET_KEY'] = "winteriscoming"
    app.run(host='0.0.0.0', debug=True)
