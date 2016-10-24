# zippy
A python script to inspect thumbnail images in zip files. Search for thumbnail.{jpg|png|jpeg|gif} in zipfiles and report image details - pixel width, height,format,color mode.

Dependencies: Python Image Library (Pillow) http://pillow.readthedocs.io

pip install Pillow

```usage: zippy.py [-h] [-f csvfile] [-p path] [-o outfile] [-v] [-w]```

Search for thumbnails in zip files and print report.

- *.zip in current dir
- *.zip in [-p path]
- zip files listed in [-f csvfile]


```optional arguments:```


```  -h, --help                  show this help message and exit```


```  -f csvfile, --file csvfile  CSV file with id,zip filename```


```  -p path, --path path        path to zip file(s)```


```  -o outfile, --out outfile   path to output file```


```  -v, --verbose               print status messages```


```  -w, --warning               disable decompression bomb warning```
  


