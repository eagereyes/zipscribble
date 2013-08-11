# ZIP Code/Post Code Data

The data in this directory is downloaded from [geonames](http://download.geonames.org/export/zip/). The `download.sh` script refreshes the files, but since it does that based on existing files, you have to manually download them first to prime the process. See the `index.html` file in the parent directory for a list of countries I've included on the website (i.e., where I feel that the data is good enough to not be too embarrassing).

# Conversion to GeoJSON

The `txt2json.py` script converts the text files from geonames to GeoJSON that can be loaded by polymaps. It also creates the countryinfo.json file that contains the bounding boxes for all the countries in the directory.
