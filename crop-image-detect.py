import os
import time
import json
import datetime
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.widgets as mwidgets
import subprocess


# get input file folder name and file name, should be optimized
images_folder = input("Please enter the images folder name: ")
# images_folder = "c:\share_with_linux"
input_file_name = input("Please enter image file name: ")
# input_file_name = "board.jpg"
input_image_file = images_folder + "\\" + input_file_name

# open input image file
image = Image.open(input_image_file)

# Convert the black-whitea image to an RGB-like format for matplotlib
rgb_image = np.array(image.convert("RGB"))

fig, ax = plt.subplots(figsize=(18,16))
plt.subplots_adjust(top=0.99, bottom=0.01, left=0.01, right=0.99, hspace=0.1, wspace=0.1)
ax.imshow(rgb_image)

def extract_text_from_json_file(file_name):
    max_attempts = 5
    wait_time = 2
    for _ in range(max_attempts):
        if os.path.exists(file_name):
            with open(file_name) as json_file:
                data = json.load(json_file)
                text = data["responses"][0]["fullTextAnnotation"]["text"]
            return text
        else:
            time.sleep(wait_time)
    print("Error: failed to get the response data from gcloud.")
    return ""

def onselect(eclick, erelease):
    box = (eclick.xdata, eclick.ydata, erelease.xdata, erelease.ydata) # box = (left, upper, right, lower)
    print(box)
    # crop the selected rectangle from input file
    cropped_image = image.crop(box)
    try:
        # save the cropped image
        cropped_file_name = images_folder + "\\croped_from_" + input_file_name.split(".")[0] + "_" + datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S') + ".jpg"
        cropped_image.save(cropped_file_name)
    except Exception:
        print("Error when save corpped image file.")
        return -1
    gcloud_output_file_name = cropped_file_name.split(".")[0] + "_result.json"
    command = f'gcloud ml vision detect-text {cropped_file_name} > {gcloud_output_file_name}'
    subprocess.run(command, shell=True)
    response_text = extract_text_from_json_file(gcloud_output_file_name)
    print("gcloud response with:")
    print(response_text)
    
props = dict(facecolor='grey', alpha=0.2)
rect = mwidgets.RectangleSelector(ax, onselect, interactive=True, props=props)
plt.show()