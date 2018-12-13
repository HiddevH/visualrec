# Written by:	# Hidde van Heijst - hpf.vanheijst@gmail.com
""" Reads the cast folders and returns them as a list.
	Each cast folder has a thumbnail which can be displayed accordingly. """ 

def get_browse_casts(search_term=''):
	""" Returns a list of casts.
	:param search_term -> The cast results should match with the search_term. """ 
	from pathlib import Path
	import glob
	import os

	rootdir = Path('static')
	cast_list = [str(os.path.basename(os.path.normpath(f))) for f in rootdir.glob('casts/*')  # If f is a folder in casts 
	                 	if f.is_dir() and search_term in str(f)]  # and not in exclude_dir, we put it in cast_list
	return cast_list

if __name__ == '__main__':
    get_browse_casts()