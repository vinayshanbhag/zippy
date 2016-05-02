# zippy
A python script to inspect zip files for thumbnail images

```Usage: zippy.py <path/to/zip/files> <path/to/output.csv [results.csv]>```

Search ```path/to/zip/files``` recursively for zip files. Inspect each zip file for at least one thumbnail image - thumbnail.{jpg|png|gif|jpeg} file in the root folder.

Print count of zip files inspected and those with/ without a thumbnail image.

Output report to a csv file - path, zip filename, status and thumbnail filename (if present).
