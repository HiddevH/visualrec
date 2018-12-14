# -*- coding: utf-8 -*-
"""Create_Encodings
Creating encodings of all cast folders placed in static/casts/ and stores them in static/encodings/



# Written by:   # Maurice Richard- mauricerichard91@gmail.com
#               # Hidde van Heijst - hpf.vanheijst@gmail.com
Special dependencies:
    !pip install cmake
    !pip install dlib
    !pip install face_recognition
"""

import face_recognition
from pathlib import Path
import pickle

def load_cast(cast_folder, encoding_path):
    """ Creates encodings for the cast located at path cast_folder
      And stores the encodings in encoding_path.
      :param cast_folder -> the folder where the cast resides
      :param encoding_path -> the path where the encoding should be stored
      """

    import face_recognition
    import glob
    import re
    import pickle

    known_image_encodings = []  # Voor de encodings
    image_names = [] # Image namen
    images = [] # De images

    for filename in glob.glob(cast_folder +'/*.jpeg'): # Must be jpegs
      if 'thumbnail' not in filename: # Don't encode thumbnails
          print(f'encoding filename: {filename}')
          images.append(filename) # List met de filenames van de cast
          im = face_recognition.load_image_file(filename) # Face recognition op de cast
          im = face_recognition.face_encodings(im)[0]
          known_image_encodings.append(im)

    encodes = dict(zip(images, known_image_encodings)) # We koppelen de bestandsnamen aan de gescande gezichten. De regex bij name =  kunnen we gebruiken om de namen uit de bestanden te halen
    pickle.dump(encodes, open(encoding_path, 'wb'))  # Schrijf de dict encodes weg naar een pickle data bestand
    print(f'Succesfully stored encodings to {encoding_path}') # Bevestig het schrijven


def create_encodings(search_term=''):
    """ This function scans the casts folder for casts, and if an face recogntion encoding already exists or not.
    If it does not exist yet, it calls to generate an encoding"""

    import numpy as np
    import re
    from pathlib import Path
    import os

    rootdir = Path('static')


    cast_list = [str(f) for f in rootdir.glob('casts/*')  # If f is a folder in casts
                         if f.is_dir() and search_term in str(f)]  # and not in exclude_dir, we put it in file_list


    for cast_folder in cast_list:
        cast = os.path.basename(os.path.normpath(cast_folder))  # strip the directory path from the cast_folder
        encoding_path =  Path(rootdir) / 'encodings' / f'{cast}_encodings.p'
        print(f'trying encode for: {cast}..')

        try:  # If an encoding already exists, we try loading it
            with open(encoding_path, 'rb') as encoded_cast:
                load_cast(cast_folder, encoding_path)  # Create encodings for the cast
                print(f'created encoding for {cast}!')
        except OSError :  # If the cast encoding is not found, we create one
            print('Something went wrong..')

if __name__ == '__main__':
    create_encodings()
