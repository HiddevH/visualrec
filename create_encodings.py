# -*- coding: utf-8 -*-
"""Face_Recognition_GoT

# Creating encodings of all cast folders
# Written by: Maurice Richard- mauricerichard91@gmail.com
Installeer de benodigde packages
    !pip install cmake
    !pip install dlib
    !pip install face_recognition
"""
def create_encodings():
    import face_recognition
    import pickle
    import numpy as np
    import re
    from pathlib import Path

    rootdir = Path('static')
    exclude_dir = ['static/Thumbnails', 'static/css']

    file_list = [str(f) for f in rootdir.glob('**/*') if f.is_dir() and str(f) not in exclude_dir]

    for cast_folder in file_list:
        print(cast_folder)
        try: # Als er al een pickle bestand bestaat van de geladen cast dan laad hij dat
            with open('{}_encodings.p'.format(cast_folder), 'rb') as cast:
                known_image_encodings = pickle.load(cast)
        except OSError : # Anders laad de cast en maak er een pickle van
            print('Cast encodings not found, creating new encodings..')
            from cast_loader import load_cast
            load_cast(cast_folder)
            known_image_encodings = pickle.load(open('{}_encodings.p'.format(cast_folder), 'rb')) # Schrijf de data in known_image_encodings

if __name__ == '__main__':
    create_encodings()
