#!/usr/bin/env python3
#
""" zippy.py
 Search for Thumbnail.{jpg,png,jpeg,gif} in zipfiles and report image details - width, height,format,color mode.
   -f csvfile (optional): csv file with id(column 1) and zip filename (column 2). Search for *.zip in path if not csvfile is not provided
   -p path (optional): location on disk where zip files are located. Current working directory if not provided
   -o outfile (optional): results output to this file in CSV format- Id (-f option only),zip filename,Thumbnail,width(px),height(px),format,color mode
 
 Dependencies: Python Image Library (Pillow) http://pillow.readthedocs.io
 pip install Pillow
 
 Vinay Shanbhag 2016
"""

import os, glob, csv, zipfile, tempfile
from argparse import ArgumentParser, RawTextHelpFormatter
from PIL import Image
outfile = 'results.csv'

parser = ArgumentParser(description='Search for thumbnails in zip files and print report.\n - *.zip in current dir\n - *.zip in [-p path]\n - zip files listed in [-f csvfile]',
                        epilog='vinay shanbhag(2016)\n', formatter_class=RawTextHelpFormatter)
parser.add_argument("-f", "--file", dest="inputfile",
                  help="CSV file with id,zip filename", metavar="csvfile")
parser.add_argument("-p", "--path", dest="path",
                  help="path to zip file(s)", metavar="path")
parser.add_argument("-o", "--out", dest="outfile",
                  help="path to output file", metavar="outfile")
parser.add_argument("-v", "--verbose",
                  dest="verbose", action='store_true',
                  help="print status messages")
parser.add_argument("-w", "--warning",
                  dest="warning", action='store_true',
                  help="disable decompression bomb warning")
args = parser.parse_args()
inputfile = args.inputfile
path = args.path + os.path.sep if args.path else ''
if args.outfile:
    outfile = args.outfile 
elif inputfile: 
    outfile = inputfile.split(os.path.sep)[-1:][0].split('.')[:-1][0] + '-results.csv'

if args.warning: Image.warnings.simplefilter('ignore', Image.DecompressionBombWarning)

# acceptable thumbnail file names
thumbnails = {'thumbnail.jpg','thumbnail.png’,’thumbnail.gif','thumbnail.jpeg'} 

# Replace archive with RGB thumbnail. 
def updateThumb(zipfilename, thumbfilename, image):
    """ Update replace thumbfilename in zipfilename with image """
    tempfd, tempname = tempfile.mkstemp(dir=os.path.dirname(zipname))
    os.close(tmpfd)            
    with zipfile.ZipFile(zipfilename, 'r') as zipsrc:
        with zipfile.ZipFile(tempname, 'w') as zipdest:
            zipdest.comment = zipsrc.comment
            for item in zipsrc.infolist():
                if item.filename != thumbfilename:
                    zipdest.writestr(item, zipsrc.read(item.filename))
    os.remove(zipfilename)
    os.rename(tempname, zipfilename)
    with zipfile.ZipFile(zipfilename, mode='a', compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(thumbfilename, image)

def printMessage(s):
    """ print messages to stdout in verbose mode """
    if args.verbose:print(s)

def parseFromPath():
    """ Inspect all zip files (not recursive) in current directory or path provided via [-p path] option """
    if path:
        searchpath = path + os.path.sep +'*.zip'
    else:
        searchpath = '*.zip'
    zipfiles = glob.glob(searchpath)
    if not zipfiles:
        print('No zip files found')
        parser.print_usage()
        exit()
    try:
        with open(outfile,'w',newline='') as cf:
            writer = csv.writer(cf,delimiter=',',quotechar='"')
            writer.writerow(['Filename','Thumbnail','Width(px)','Height(px)','Format','Color Mode'])
            for name in zipfiles:
                try:
                    printMessage('inspecting ' + name)
                    zip = zipfile.ZipFile(name)
                    filenames = {n for n in zip.namelist()}
                    if filenames.intersection(thumbnails):
                        thumb = filenames.intersection(thumbnails).pop()
                        printMessage('  Found ' + thumb)
                        try:
                            with zip.open(thumb) as tf:
                                img = Image.open(tf)
                                printMessage('  (' + str(img.size[0]) + 'x' + str(img.size[1]) + ')px, ' +img.format + ' ' + img.mode)
                                writer.writerow([name,thumb, img.size[0],img.size[1],img.format,img.mode])
                                #if img.mode = 'CMYK': updateThumb(path+row[1],thumb,img.convert('RGB'))
                                img.close()
                        except IOError:
                            printMessage('  Failed to open')
                            writer.writerow([name,'Failed to open '+thumb, 'NA','NA','NA','NA'])
                    else:
                        printMessage('  No Thumbnail')
                        writer.writerow([name,'No Thumbnail', 'NA','NA','NA','NA'])
                    zip.close()
                except IOError: 
                    printMessage('ZIP File Not Found ' + name)
                    writer.writerow([name,'ZIP File Not found','NA','NA','NA','NA'])
                except zipfile.BadZipFile:
                    printMessage('Bad ZIP File ' + name)
                    writer.writerow([name,'Bad ZIP File','NA','NA','NA','NA'])
                finally:
                    cf.flush()
            print('\nSee %s'%outfile)
    except IOError: 
        print('Cannot write to %s'%outfile)
        exit()
        
def parseFromFile():
    """ Parse input CSV file provided via [-f csvfile] option for zip filenames. Inspect zip files from csvfile in path [-p path] or current directory"""
    try:
        with open(inputfile,'r') as cf:
            data = [d for d in csv.reader(cf,delimiter=',',quotechar='"')]
    except IOError: 
        print('Error reading input file %s\nExpect CSV file with unique id(column 1) and zip filename (column 2)'%inputfile)
        exit()
    try:
        with open(outfile,'w',newline='') as cf:
            writer = csv.writer(cf,delimiter=',',quotechar='"')
            writer.writerow(['Unique ID','Filename','Thumbnail','Width(px)','Height(px)','Format','Color Mode'])
            for row in data:
                try:
                    printMessage('Inspecting ' + path+row[1])
                    zip = zipfile.ZipFile(path+row[1])
                    filenames = {n for n in zip.namelist()}
                    if filenames.intersection(thumbnails):
                        thumb = filenames.intersection(thumbnails).pop()
                        printMessage('  Found ' + thumb)
                        try:
                            with zip.open(thumb) as tf:
                                img = Image.open(tf)
                                printMessage('  (' + str(img.size[0]) + 'x' + str(img.size[1]) + ')px, ' +img.format + ' ' + img.mode)
                                writer.writerow([row[0],row[1],thumb, img.size[0],img.size[1],img.format,img.mode])
                                #if img.mode = 'CMYK': updateThumb(path+row[1],thumb,img.convert('RGB'))
                                img.close()
                        except IOError:
                            printMessage('  Failed to open')
                            writer.writerow([row[0],row[1],'Failed to open '+thumb, 'NA','NA','NA','NA'])
                    else:
                        printMessage('  No Thumbnail')
                        writer.writerow([row[0],row[1],'No Thumbnail', 'NA','NA','NA','NA'])
                    zip.close()
                except IOError: 
                    printMessage('ZIP File Not Found ' + path+row[1])
                    writer.writerow([row[0],row[1],'ZIP File Not Found','NA','NA','NA','NA'])
                except zipfile.BadZipFile:
                    printMessage('Bad ZIP File ' + name)
                    writer.writerow([row[0],row[1],'Bad ZIP File','NA','NA','NA','NA'])
                finally:
                    cf.flush()
            print('\nSee %s'%outfile)
    except IOError: 
        print('Cannot write to %s'%outfile)
        exit()

if inputfile:
    print('Parsing %s for zip files'%inputfile)
    parseFromFile()
else:
    print('Searching %s for zip files'% (path if path else os.getcwd()))
    parseFromPath()
