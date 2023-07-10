import numpy as np
import os
import matplotlib.pyplot as plt
from tifffile import imread, imwrite, imshow

control_path = input("Enter the path to the CONTROL image: ")
red_path = input("Enter the path to the RED channel image: ")
green_path = input("Enter the path to the GREEN channel image: ")
blue_path = input("Enter the path to the BLUE channel image: ")

# Load the images as 2D numpy arrays
paths_tuple = (control_path, red_path, green_path, blue_path)
images_list = []
for path in paths_tuple:
    image = imread(path)
    if image.ndim > 2:
        image = image[:,:,0]
    images_list.append(image)

# Adjust the channel brightness and contrast
adjusted_images = []
for image in images_list:
    image = image - image.min()
    image = image / image.max()
    adjusted_images.append(image)

# Subtract control image from colour channel images
control_image = images_list[0]
rgb_images = []
for image in images_list[1:]:
    adjusted_image = image - control_image
    adjusted_image[adjusted_image < 0] = 0
    rgb_images.append(adjusted_image)

colour_image = np.stack(rgb_images)
imshow(colour_image, cmap="gray")
plt.show()

# Save images
parent_path = control_path.rsplit("/", 1)[0]
colour_path = os.path.join(parent_path, "overlaid_control_adjusted.tif")
control_path = os.path.join(parent_path, "adjusted_control.tif")

imwrite(colour_path, colour_image)
imwrite(control_path, control_image)