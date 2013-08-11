#!/bin/bash
rm readme.txt
for i in ??.txt; do
  curl -O http://download.geonames.org/export/zip/`basename $i .txt`.zip
  unzip -o `basename $i .txt`.zip $i
  rm `basename $i .txt`.zip
done
curl -O http://download.geonames.org/export/zip/readme.txt

