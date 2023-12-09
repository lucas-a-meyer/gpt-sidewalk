import json
import os

base_url = "https://github.com/lucas-a-meyer/gpt-sidewalk/blob/main"

# iterate over the curb_ramp and no_curb_ramp directories and
# create JSON objects with the image URL and the directory

file_list = []
for directory in ["curb_ramp", "no_curb_ramp"]:
    for filename in os.listdir(directory):
        if filename.endswith(".jpeg"):
            file_list.append({"url": f"{base_url}/{directory}/{filename}?raw=true", "ground_truth_has_curb_ramp": directory == "curb_ramp"})
            
# write the list to a file
with open("curb_ramp_list.json", "w") as f:
    json.dump(file_list, f, indent=4)

