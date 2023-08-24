import os
import json
import time
import datetime
import subprocess
import numpy as np
import pyperclip
import tkinter as tk
import matplotlib.pyplot as plt

from tkinter import filedialog, messagebox


def open_file_dialog():
    root = tk.Tk()
    root.withdraw()
    path = filedialog.askopenfilename()
    
    if path is None:
        return None
    
    # change the path string to windows format
    path = path.replace("/", "\\")
    
    # divide path into folder name and file name
    path_divided = path.rsplit("\\", 1)
    folder_name = path_divided[0]
    file_name = path_divided[1]
    return (path, folder_name, file_name)

def convert_to_rgb_image(image):
    return np.array(image.convert("RGB"))

def prepare_plot(image, fig_width=18, fig_height=16):
    fig, ax = plt.subplots(figsize=(fig_width,fig_height))
    plt.subplots_adjust(top=0.99, bottom=0.01, left=0.01, right=0.99, hspace=0.1, wspace=0.1)
    ax.imshow(image)
    return (fig, ax)

def detect_image(box, image, images_folder, input_file_name):
    
    # crop the selected rectangle from input file
    cropped_image = image.crop(box)
    try:
        # save the cropped image
        cropped_file_name = images_folder + "\\croped_from_" + input_file_name.split(".")[0] + "_" + datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S') + ".jpg"
        cropped_image.save(cropped_file_name)
        return cropped_file_name
    except Exception:
        print("Error when save corpped image file.")
        return ""

def gcloud_querey(cropped_file_name):
    gcloud_output_file_name = cropped_file_name.split(".")[0] + "_result.json"
    command = f'gcloud ml vision detect-text {cropped_file_name} > {gcloud_output_file_name}'
    subprocess.run(command, shell=True)
    return gcloud_output_file_name
    

def extract_text_from_json_file(file_name):
    print(file_name)
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

def show_response(response_text):
    messagebox.showinfo("Gcloud response with:", response_text)
    # copy response_text to system
    pyperclip.copy(response_text)
