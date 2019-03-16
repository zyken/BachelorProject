#!/bin/bash

# creates tif file for all cr2 files in a folder

#usage: ./convert_cr2_to_tif.sh path_to_folder/ path_to_save_folder/

folder="$1"
out_path="$2"

# processes raw files
for f in $folder*.CR2;
do
        echo "Processing $f"
        ufraw-batch \
                --out-type=tif \
                --out-path=$out_path \
                $f
done;