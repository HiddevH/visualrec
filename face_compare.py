# -*- coding: utf-8 -*-
"""Face_Recognition_GoT

# Game of Thrones Look-A-Like
# Written by: Hidde van Heijst - hidde@vanheijst.com
Installeer de benodigde packages
    !pip install cmake
    !pip install dlib
    !pip install face_recognition
"""

import PIL
from PIL.ExifTags import TAGS as EXIFTAGS
import face_recognition
import pickle
import numpy as np
import re
from pathlib import Path
import os

def rotate_convert_image(file, mode='RGB'):
    """
    Images uploaded by Mobile OS usually are rotated in some way (EXIF), 
    this causes the script to not find any matches.
    This script checks if an EXIF tag exists, then fixes correspondingly.
    Then converts an image file (.jpg, .png, etc) into a numpy array
    :param file: image file name or file object to load
    :param mode: format to convert the image to. Only 'RGB' (8-bit RGB, 3 channels) and 'L' (black and white) are supported.
    :return: image contents as numpy array
    """

    image = PIL.Image.open(file) # Open the image with PIL

    # If no ExifTags, no rotating needed.
    try:
       # Grab orientation value.
       image_exif = image._getexif()
       image_orientation = image_exif[274]

       # Rotate depending on orientation.
       if image_orientation == 2:
          image = image.transpose(PIL.Image.FLIP_LEFT_RIGHT)
       if image_orientation == 3:
          image = image.transpose(PIL.Image.ROTATE_180)
       if image_orientation == 4:
          image = image.transpose(PIL.Image.FLIP_TOP_BOTTOM)
       if image_orientation == 5:
          image = image.transpose(PIL.Image.FLIP_LEFT_RIGHT).transpose(PIL.Image.ROTATE_90)
       if image_orientation == 6:
          image = image.transpose(PIL.Image.ROTATE_270)
       if image_orientation == 7:
          image = image.transpose(PIL.Image.FLIP_TOP_BOTTOM).transpose(PIL.Image.ROTATE_90)
       if image_orientation == 8:
          image = image.transpose(PIL.Image.ROTATE_90)
    except:
       pass

    if mode:
        image = image.convert(mode)  # Format the image
    return np.array(image)  # Return numpy array of image


def face_recog(usr_image):
    """
    Scans photo uploaded by User and detects faces.
    If only one face is found, we use it to match with casts.
    Otherwise, this function returns an empty dict and an error message."""

    rootdir = Path('static')
    exclude_dir = ['nietdezefolder']  # If you want to exclude some paths
    cast_list = [str(f) for f in rootdir.glob('casts/*')  # If f is a folder in casts
                         if f.is_dir() and str(f) not in exclude_dir]  # and not in exclude_dir, we put it in file_list

    results = {}  # We want to store a result for each cast, in a dict
    error = '' # Empty error message
    unknown = usr_image # Dit is het geüploade bestand
    unknown_image = rotate_convert_image(unknown) # Rotate and convert image to numpy array
    unknown_image_encodings = face_recognition.face_encodings(unknown_image)
    if len(unknown_image_encodings) == 0:  # if no faces are detected
        error = 'No faces detected in the image. Please try another photo.'
    elif len(unknown_image_encodings) > 1:  # if more than one faces are deteced
        error = 'Multiple faces detected in the image. Please upload a photo with one face.'
    else:
        unknown_encoding = unknown_image_encodings[0] # Face_recognition op unknown

        for cast_folder in cast_list:
            # < THIS CODE IS MOSTLY SAME AS create_encodings.py >
            cast = os.path.basename(os.path.normpath(cast_folder))  # strip the directory path from the cast_folder
            encoding_path =  Path(rootdir) / 'encodings' / f'{cast}_encodings.p'  # generate the encoding path for the cast

            try:  # If an encoding already exists, we try loading it
                with open(encoding_path, 'rb') as encoded_cast:
                    known_image_encodings = pickle.load(encoded_cast)
            except IOError: # If it doesn't exist, send an email to tech support? :-D
            # We need to revamp this 
                from error_email import errormail
                subject = f'IMAGINE_DS: Error occured in face_compare.py'
                message = f'User tried loading the cast of {cast_folder} but failed.'
                errormail(subject=subject, msg=message)


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
    print(error)
    return(results, error) # Return de resultaten en evt error message

if __name__ == "__main__":
    face_recog('donald.jpg')
