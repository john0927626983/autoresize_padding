import cv2
import numpy as np
import os
import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox

def process_images():
    folder_path = input_folder_var.get()
    output_folder = output_folder_var.get()
    new_image_width = int(width_var.get())
    new_image_height = int(height_var.get())
    color = color_var.get()

    # Convert color from hex to BGR
    color_bgr = tuple(int(color[i:i+2], 16) for i in (5, 3, 1))

    # Ensure output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(folder_path):
        if filename.endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tiff')):
            img_path = os.path.join(folder_path, filename)
            img = cv2.imread(img_path)

            if img is None:
                print(f"Error reading {filename}, skipping.")
                continue

            old_image_height, old_image_width, channels = img.shape
            aspect_ratio = old_image_width / old_image_height

            # Determine the new dimensions based on aspect ratio
            if aspect_ratio > 1:
                new_width = new_image_width
                new_height = int(new_image_width / aspect_ratio)
            else:
                new_height = new_image_height
                new_width = int(new_image_height * aspect_ratio)

            # Ensure dimensions don't exceed target canvas size
            if new_height > new_image_height:
                new_height = new_image_height
                new_width = int(new_image_height * aspect_ratio)
            if new_width > new_image_width:
                new_width = new_image_width
                new_height = int(new_image_width / aspect_ratio)

            resized_img = cv2.resize(img, (new_width, new_height))
            result = np.full((new_image_height, new_image_width, channels), color_bgr, dtype=np.uint8)

            # Compute center offset for padding
            x_center = (new_image_width - new_width) // 2
            y_center = (new_image_height - new_height) // 2

            result[y_center:y_center + new_height, x_center:x_center + new_width] = resized_img

            output_path = os.path.join(output_folder, f"padded_{filename}")
            cv2.imwrite(output_path, result)

    messagebox.showinfo("Processing Complete", "Images have been processed and saved to the output folder.")

# GUI setup
root = tk.Tk()
root.title("Image Resizer with Padding")

# Input Folder
tk.Label(root, text="Input Folder").grid(row=0, column=0, sticky="e")
input_folder_var = tk.StringVar()
tk.Entry(root, textvariable=input_folder_var, width=50).grid(row=0, column=1)
tk.Button(root, text="Browse", command=lambda: input_folder_var.set(filedialog.askdirectory())).grid(row=0, column=2)

# Output Folder
tk.Label(root, text="Output Folder").grid(row=1, column=0, sticky="e")
output_folder_var = tk.StringVar()
tk.Entry(root, textvariable=output_folder_var, width=50).grid(row=1, column=1)
tk.Button(root, text="Browse", command=lambda: output_folder_var.set(filedialog.askdirectory())).grid(row=1, column=2)

# Image Width
tk.Label(root, text="New Image Width").grid(row=2, column=0, sticky="e")
width_var = tk.StringVar(value="1024")
tk.Entry(root, textvariable=width_var).grid(row=2, column=1, sticky="w")

# Image Height
tk.Label(root, text="New Image Height").grid(row=3, column=0, sticky="e")
height_var = tk.StringVar(value="768")
tk.Entry(root, textvariable=height_var).grid(row=3, column=1, sticky="w")

# Padding Color
tk.Label(root, text="Padding Color").grid(row=4, column=0, sticky="e")
color_var = tk.StringVar(value="#FFFFFF")  # Default to white
tk.Entry(root, textvariable=color_var, width=10).grid(row=4, column=1, sticky="w")
tk.Button(root, text="Choose Color", command=lambda: color_var.set(colorchooser.askcolor()[1])).grid(row=4, column=2)

# Process Button
tk.Button(root, text="Process Images", command=process_images).grid(row=5, column=1, pady=10)

root.mainloop()

'''
import cv2
import numpy as np
import os

# Define the path to the folder containing images
folder_path = 'Spirits_Liquors_4'
output_folder = 'output_folder'

# Ensure output folder exists
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Define new dimensions and padding color
new_image_width = 1024
new_image_height = 768
color = (255, 255, 255)  # white padding

# Loop through all files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tiff')):  # Acceptable image formats
        # Read image
        img_path = os.path.join(folder_path, filename)
        img = cv2.imread(img_path)

        if img is None:
            print(f"Error reading {filename}, skipping.")
            continue

        old_image_height, old_image_width, channels = img.shape

        # Calculate the aspect ratio of the original image
        aspect_ratio = old_image_width / old_image_height

        # Determine the new dimensions based on aspect ratio
        if aspect_ratio > 1:  # Image is wider than it is tall
            new_width = new_image_width
            new_height = int(new_image_width / aspect_ratio)
        else:  # Image is taller than it is wide
            new_height = new_image_height
            new_width = int(new_image_height * aspect_ratio)

        # Ensure the new dimensions don't exceed the target canvas size
        if new_height > new_image_height:
            new_height = new_image_height
            new_width = int(new_image_height * aspect_ratio)
        if new_width > new_image_width:
            new_width = new_image_width
            new_height = int(new_image_width / aspect_ratio)

        # Resize the image to fit within the canvas
        resized_img = cv2.resize(img, (new_width, new_height))

        # Create a blank image with the new size and the padding color
        result = np.full((new_image_height, new_image_width, channels), color, dtype=np.uint8)

        # Compute center offset for padding
        x_center = (new_image_width - new_width) // 2
        y_center = (new_image_height - new_height) // 2

        # Insert the resized image into the center of the result image
        result[y_center:y_center + new_height, x_center:x_center + new_width] = resized_img

        # Save the result image
        output_path = os.path.join(output_folder, f"padded_{filename}")
        cv2.imwrite(output_path, result)
        #print(f"Saved padded image: {output_path}")

print("Processing complete.")
'''
