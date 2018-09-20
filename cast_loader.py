# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 11:20:47 2018

@author: Hidde
"""


def load_cast(cast_folder):
    import face_recognition
    import glob
    import re
    import pickle
    
    #cast_folder = 'Game_of_Thrones'  # In je directory deze folder zetten
    
    known_image_encodings = []  # Voor de encodings
    image_names = [] # Image namen
    images = [] # De images
    
    for filename in glob.glob(cast_folder +'/*.jpeg'): #jpegs
          name = re.sub('(^[^\\\]*[^_])', '', filename)
          name = re.sub('\.jpeg$', '', name) # Haalt de namen uit de bestandsnamen
          print(filename)
          image_names.append(name) # List met de namen van de cast
          images.append(filename) # List met de filenames van de cast
          im = face_recognition.load_image_file(filename) # Face recognition op de cast
          im = face_recognition.face_encodings(im)[0]
          known_image_encodings.append(im)
          
    encodes = dict(zip(images, known_image_encodings)) # We koppelen de bestandsnamen aan de gescande gezichten. De regex bij name =  kunnen we gebruiken om de namen uit de bestanden te halen
    
    pickle_file = '{}_encodings.p'.format(cast_folder) # Definieer pickle bestandsnaam
    pickle.dump(encodes, open(pickle_file, 'wb'))  # Schrijf de dict encodes weg naar een pickle data bestand
    print('Succesfully stored encodings to ' +pickle_file) # Bevestig het schrijven
    
    #known_image_encodings = pickle.load(open('{}_encodings.p'.format(cast_folder), 'rb')) # Zo open je het bovenstaand opgeslagen pickle bestand

#load_cast('Game_of_Thrones') 