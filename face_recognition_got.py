# -*- coding: utf-8 -*-
"""Face_Recognition_GoT

# Game of Thrones Look-A-Like
# Written by: Hidde van Heijst - hidde@vanheijst.com
Installeer de benodigde packages
    !pip install cmake
    !pip install dlib
    !pip install face_recognition
"""


import face_recognition
import glob
import re

cast_folder = 'Game_of_Thrones'  # In je directory deze folder zetten

known_image_encodings = []  # Voor de encodings
image_names = [] # Image namen
images = [] # De images

for filename in glob.glob(cast_folder +'/*.jpeg'): #jpegs
      name = re.sub('(^[^\\\]*[^_])', '', filename)
      name = re.sub('\.jpeg$', '', name) # Haalt de namen uit de bestandsnamen
      print(filename)
      image_names.append(name)
      images.append(filename)
      im = face_recognition.load_image_file(filename)
      im = face_recognition.face_encodings(im)[0]
      known_image_encodings.append(im)

print('Cast succesfully loaded')
      
# own_image = je eigen plaat
def face_recog(own_image):  
    unknown = own_image
    
    from IPython.display import Image
    unknown_image = face_recognition.load_image_file(unknown)
    unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
    print('Scanning faces ..')
    #print('Inserted the following image:')
    #Image(filename=unknown)
    
    import numpy as np
    
    face_distances = face_recognition.face_distance(known_image_encodings, unknown_encoding)
    best_match = np.argmin(face_distances)
    name = image_names[best_match]
    return_img = Image(filename=images[best_match])    
    return(name, return_img)

#==============================================================================
# name, image = face_recog('donald.jpg')   # Donald is onze testman ;-)
# print("You most closely look like:" , name) # Er komt een lege naam terug omdat de regex nog niet werkt..
# image
#==============================================================================


# =============================================================================
#     """OVERIGE SHIT"""
#     
#     for i, face_distance in enumerate(face_distances):
#         print("The test image has a distance of {:.2} from known image #{}".format(face_distance, i))
#         print("- With a normal cutoff of 0.6, would the test image match the known image? {}".format(face_distance < 0.6))
#         print("- With a very strict cutoff of 0.5, would the test image match the known image? {}".format(face_distance < 0.5))
#         print()
#     
#     # biden_encoding = face_recognition.face_encodings(known_image)[0]
#     unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
#     
#     results = face_recognition.compare_faces(known_image_encodings, unknown_encoding)
#     
#     look_like = []
#     if True in results:
#       first_match_index = results.index(True)
#       img = images[first_match_index]
#       print(img)
#     
#     from IPython.display import Image 
#     print('Found a match! See below:')
#     Image(filename=img)
#     
#     print(results)
# =============================================================================
    


