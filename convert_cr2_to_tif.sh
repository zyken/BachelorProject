#!/bin/bash

# creates tif file for all cr2 files in a folder

#usage: ./convert_cr2_to_tif.sh path_to_folder/

folder="$1"

# processes raw files
for f in $folder*.CR2;
do
        echo "Processing $f"
        ufraw-batch \
                --out-type=tif \
                --out-path=. \
                $f
done;