#!/usr/bin/env python3
#
# zippy.py
# Usage: zippy.py <path/to/zip/files> <output file name [results.csv]>
# Search specified path recursively for zip files. Inspect each zip file for a thumbnail image - thumbnail.{jpg|png|gif|jpeg} file in the root folder.
# Print count of zip files with or without a thumbnail image
# Output path, filename, thumbnail file name to a CSV file
#
# Vinay Shanbhag 
#

import os
import sys
import glob
import zipfile

absolutepath = '' # Absolute path to search for zip files
thumbnails = frozenset(['thumbnail.jpg','thumbnail.png’,’thumbnail.gif','thumbnail.jpeg']) # acceptable thumbnail file names
csvfile = 'results.csv'
wildcard = '/**/*.zip'
results = []

passcount = 0
failcount = 0

if len(sys.argv) > 1:
	absolutepath = sys.argv[1]
	searchpath = absolutepath + wildcard
	zipfiles = glob.glob(searchpath, recursive=True)
	if len(sys.argv)>2:
		csvfile = sys.argv[2]
	for file in zipfiles:
		zip = zipfile.ZipFile(file)

		# Ignore path - accept thumbnails nested in folders
		# filenames = [os.path.basename(x) for x in zip.namelist()]
		
		# Ignore case - accept thumbnail file names with mixed case
		# filenames = set([x.lower() for x in zip.namelist()]) 

		# Case sensitive names. Accept thumbnails only in the root folder of the zip file
		filenames = set(zip.namelist())

		if len(filenames.intersection(thumbnails)) > 0: # At least one thumbnail 
			results.append(os.path.dirname(file) + ',' + os.path.basename(file) + ',PASS,' + filenames.intersection(thumbnails).pop())
			#print(file, ',PASS,',filenames.intersection(thumbnails))
			passcount += 1
		else:
			results.append(os.path.dirname(file) + ',' + os.path.basename(file) + ',FAIL,Not Available')
			#print(file, ',FAIL,NA')
			failcount += 1
	f = open(csvfile,'w')
	f.write('Path,ZIP File Name,Status,Thumbnail\n')
	for line in results:
		f.write(line+'\n')
	f.close()
	print('\nZippy found',len(zipfiles),'zip files in', absolutepath,'\n', passcount,'have thumbnails\n', failcount,'are missing thumbnails\n\nDetails exported to', csvfile,'\n')
else:
	print('Usage: zippy.py <path/to/zip/files> <output file name [results.csv]>')