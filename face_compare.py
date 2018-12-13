# -*- coding: utf-8 -*-
"""Face_Recognition_GoT

# Game of Thrones Look-A-Like
# Written by: Hidde van Heijst - hidde@vanheijst.com
Installeer de benodigde packages
    !pip install cmake
    !pip install dlib
    !pip install face_recognition
"""

def face_recog(usr_image):
    import face_recognition
    import pickle
    import numpy as np
    import re
    from pathlib import Path
    import os


    rootdir = Path('static')
    exclude_dir = ['nietdezefolder']  # If you want to exclude some paths
    cast_list = [str(f) for f in rootdir.glob('casts/*')  # If f is a folder in casts 
                         if f.is_dir() and str(f) not in exclude_dir]  # and not in exclude_dir, we put it in file_list

    results = {}  # We want to store a result for each cast, in a dict

    for cast_folder in cast_list:
        # < THIS CODE IS MOSTLY SAME AS create_encodings.py >
        cast = os.path.basename(os.path.normpath(cast_folder))  # strip the directory path from the cast_folder
        encoding_path =  Path(rootdir) / 'encodings' / f'{cast}_encodings.p'  # generate the encoding path for the cast

        try:  # If an encoding already exists, we try loading it
            with open(encoding_path, 'rb') as encoded_cast:
                known_image_encodings = pickle.load(encoded_cast)
        except IOError: # If it doesn't exist, send an email to tech support? :-D
            from error_email import errormail
            subject = f'IMAGINE_DS: Error occured in face_compare.py' 
            message = f'User tried loading the cast of {cast_folder} but failed.' 
            errormail(subject=subject, msg=message)
            
        unknown = usr_image # Dit is het geüploade bestand
        unknown_image = face_recognition.load_image_file(unknown)
        unknown_encoding = face_recognition.face_encodings(unknown_image)[0] # Face_recognition op unknown
        print(f'Scanning faces in {cast}')

        face_values = list(known_image_encodings.values()) # Maak een lijst met alleen de waarden (face_encodings)
        face_distances = face_recognition.face_distance(face_values, unknown_encoding) # Bereken de afstand tussen de gezichten van de cast en het onbekende img
        best_match = np.argmin(face_distances) # Zoek de image met de minste afstand tot de onbekende image
        match_file = list(known_image_encodings.keys())[best_match] # geef de image file terug die het meest lijkt op de onbekende
        name = re.sub('(^[^\\/]*.[^\\/]*.[^\\/]*[^_])', '', match_file)
        name = re.sub('\.jpeg$', '', name) # Haalt de namen uit de bestandsnamen
        img_location = match_file # Returns filename van matched image
        results[cast] = name # We store the result in the results dict

    print(results)
    return(results) # Return de naam en bestandsnaam van de match

if __name__ == "__main__":
    face_recog('donald.jpg')

