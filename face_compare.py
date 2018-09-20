# -*- coding: utf-8 -*-
"""Face_Recognition_GoT

# Game of Thrones Look-A-Like
# Written by: Hidde van Heijst - hidde@vanheijst.com
Installeer de benodigde packages
    !pip install cmake
    !pip install dlib
    !pip install face_recognition
"""

def face_recog(own_image, cast_folder):  
    import face_recognition
    import pickle
    import numpy as np
    import re
    #from IPython.display import Image
    
    try: # Als er al een pickle bestand bestaat van de geladen cast dan laad hij dat
        with open('{}_encodings.p'.format(cast_folder), 'rb') as cast:
            known_image_encodings = pickle.load(cast)
    except IOError: # Anders laad de cast en maak er een pickle van
        print('Cast encodings not found, creating new encodings..')
        from cast_loader import load_cast
        load_cast(cast_folder)
        known_image_encodings = pickle.load(open('{}_encodings.p'.format(cast_folder), 'rb')) # Schrijf de data in known_image_encodings
      
    unknown = own_image # Dit is het geüploade bestand
    
    unknown_image = face_recognition.load_image_file(unknown)
    unknown_encoding = face_recognition.face_encodings(unknown_image)[0] # Face_recognition op unknown
    print('Scanning faces ..')
    #print('Inserted the following image:')
    #Image(filename=unknown)
    
    face_values = list(known_image_encodings.values()) # Maak een lijst met alleen de waarden (face_encodings) 
    face_distances = face_recognition.face_distance(face_values, unknown_encoding) # Bereken de afstand tussen de gezichten van de cast en het onbekende img
    best_match = np.argmin(face_distances) # Zoek de image met de minste afstand tot de onbekende image
    match_file = list(known_image_encodings.keys())[best_match] # geef de image file terug die het meest lijkt op de onbekende
    name = re.sub('(^[^\\\]*[^_])', '', match_file)
    name = re.sub('\.jpeg$', '', name) # Haalt de namen uit de bestandsnamen
    
    return_img = match_file # Returns filename van matched image - Python display: Image(filename=match_file)  
    return(name, return_img) # Return de naam en bestandsnaam van de match

#name, image = face_recog('donald.jpg', 'Game_of_Thrones')
#print("You most closely look like:" , name) # Er komt een lege naam terug omdat de regex nog niet werkt..
#image