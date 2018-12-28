# Written by:	# Hidde van Heijst - hpf.vanheijst@gmail.com
""" Reads the cast folders and returns them as a list.
	Each cast folder has a thumbnail which can be displayed accordingly.
	Counts the number of encodings en each encoding file to know how many actors a face is compared to. """ 

from pathlib import Path
import glob
import os
import pickle

rootdir = Path('static')

def get_cast_count():
	""" Returns a dict with a cast count for all encoded casts"""
	count_dict = {}
	count_path =  Path(rootdir) / 'other' / 'cast_count.p' # the place where the cast_count pickle is stored
	if os.path.exists(count_path): # It should exist
		with open(count_path, 'rb') as handle:
			count_dict = pickle.load(handle) 
	return count_dict

def get_browse_casts(search_term=''):
	""" Returns a list of casts, and counts the number of castmembers.
	:param search_term -> The cast results should match with the search_term. """ 

	cast_list = [str(os.path.basename(os.path.normpath(f))) for f in rootdir.glob('casts/*')  # If f is a folder in casts 
	                 	if f.is_dir() and search_term in str(f)]  # and not in exclude_dir, we put it in cast_list
	return cast_list

if __name__ == '__main__':
    get_browse_casts()