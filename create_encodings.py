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
          name = re.sub('(^[^\\/]*.[^\\/]*[^_])', '', filename)
          name = re.sub('\.jpeg$', '', name) # Haalt de namen uit de bestandsnamen
          print(filename)
          image_names.append(name) # List met de namen van de cast
          images.append(filename) # List met de filenames van de cast
          im = face_recognition.load_image_file(filename) # Face recognition op de cast
          im = face_recognition.face_encodings(im)[0]
          known_image_encodings.append(im)

    encodes = dict(zip(images, known_image_encodings)) # We koppelen de bestandsnamen aan de gescande gezichten. De regex bij name =  kunnen we gebruiken om de namen uit de bestanden te halen

    pickle.dump(encodes, open(encoding_path, 'wb'))  # Schrijf de dict encodes weg naar een pickle data bestand
    print(f'Succesfully stored encodings to {encoding_path}') # Bevestig het schrijven


def create_encodings():
    """ This function scans the casts folder for casts, and if an face recogntion encoding already exists or not.
    If it does not exist yet, it calls to generate an encoding"""

    import numpy as np
    import re
    from pathlib import Path
    import os

    rootdir = Path('static')
    exclude_dir = ['nietdezefolder']  # If you want to exclude some paths

    cast_list = [str(f) for f in rootdir.glob('casts/*')  # If f is a folder in casts 
                         if f.is_dir() and str(f) not in exclude_dir]  # and not in exclude_dir, we put it in file_list

    
    for cast_folder in cast_list:
        cast = os.path.basename(os.path.normpath(cast_folder))  # strip the directory path from the cast_folder
        encoding_path =  Path(rootdir) / 'encodings' / f'{cast}_encodings.p'
        print(f'looking up encoding for: {cast}..')

        try:  # If an encoding already exists, we try loading it
            with open(encoding_path, 'rb') as encoded_cast:
                known_image_encodings = pickle.load(encoded_cast)
                print(f'found the encoding for {cast}!')
        except OSError :  # If the cast encoding is not found, we create one
            print('Cast encodings not found, creating new encodings..')
            load_cast(cast_folder, encoding_path)  # Create encodings for the cast
            known_image_encodings = pickle.load(open(encoding_path, 'rb'))  # Load the data from the now encoded cast
            print(f'Succesfully loaded the newly created encodings for {cast}')  # Print a confirmation

if __name__ == '__main__':
    create_encodings()
