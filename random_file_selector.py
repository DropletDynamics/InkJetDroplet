import os
import re
import glob
import shutil
import random
import add_metadata_to_image as amdi

## Define the folder path and the file pattern
folder = "captures"#_main  selected
pattern = "images_V1-*_V2-*_V3-*_w1-*_w2-*_w3-*_d1-*_d2-*.jpg"

OutputFolder = "selected"

# Get the list of image files
files = glob.glob(folder + "/" + pattern)
print(f"Found {len(files)} image files matching the pattern")

selected_files = random.sample(files, 20)
for file in selected_files: # files: # 
    match = re.search("V1-([+-]?\\d+)_V2-([+-]?\\d+)_V3-([-+]?\\d+)_w1-(\\d+)_w2-(\\d+)_w3-(\\d+)_d1-(\\d+)_d2-(\\d+)", file)
    if match:
        V1 = match.group(1)
        V2 = match.group(2)
        V3 = match.group(3)
        w1 = match.group(4)
        w2 = match.group(5)
        w3 = match.group(6)
        d1 = match.group(7)
        d2 = match.group(8)
        # vars = [V1, V2, V3, w1, w2, w3, d1, d2]
        # vars = [float(v) for v in vars]
        vars = {'V1': int(V1), 'V2': int(V2), 'V3': int(V3), 'w1': int(w1), 'w2': int(w2), 'w3': int(w3), 'd1': int(d1), 'd2': int(d2)}
        amdi.add_metadata_tags(file, vars)
        # vars1 = amdi.read_metadata_tags(file)
        # print(vars, vars1)
        shutil.copy(file, OutputFolder)
        