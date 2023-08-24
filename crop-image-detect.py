from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.widgets as mwidgets

import utils

# use a dialog to choose input image file
path_folder_file = utils.open_file_dialog()

if path_folder_file is None:
    print("Error: can't find the specified file!")
    exit(1)

(input_image_file, images_folder, input_file_name) = path_folder_file

# open input image file
image = Image.open(input_image_file)

# Convert the black-whitea image to an RGB-like format for matplotlib
rgb_image = utils.convert_to_rgb_image(image)

fig, ax = utils.prepare_plot(rgb_image)


def onselect(eclick, erelease):
    box = (eclick.xdata, eclick.ydata, erelease.xdata, erelease.ydata) # box = (left, upper, right, lower)
    cropped_file_name = utils.detect_image(box, image, images_folder, input_file_name)
    if cropped_file_name != "":
        gcloud_output_file_name = utils.gcloud_querey(cropped_file_name)
        response_text = utils.extract_text_from_json_file(gcloud_output_file_name)
        if response_text != "":
            utils.show_response(response_text)

props = dict(facecolor='yellow', alpha=0.2)
rect = mwidgets.RectangleSelector(ax, onselect, interactive=True, props=props)
plt.show()