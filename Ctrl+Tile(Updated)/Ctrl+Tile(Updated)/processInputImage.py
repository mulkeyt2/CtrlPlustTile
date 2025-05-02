from PIL import Image, ImageOps
import os
import sys

FIXED_RESOLUTION = (1000, 1000) 

# Load and split the input image into tiles
# adjusted so that image would be resized to a consistent size. tile sizes of input images
# have been different accross images based on their resolution
# Function splits the input image into tiles of the specified size
def split_image(image, tile_size):
    # Resize the image while maintaining aspect ratio
    image = ImageOps.contain(image, FIXED_RESOLUTION)

    # Calculate the number of rows and columns
    rows = image.height // tile_size[1]
    cols = image.width // tile_size[0]

    # Split the image into tiles
    tiles = []
    for r in range(rows):
        for c in range(cols):
            left = c * tile_size[0]
            upper = r * tile_size[1]
            right = left + tile_size[0]
            lower = upper + tile_size[1]
            tile = image.crop((left, upper, right, lower))
            tiles.append(tile)

    return tiles, rows, cols

# Get the input image
def load_input_image(project_path):
    input_img_path = os.path.join(project_path, 'Input_Image')
    input_files = [f for f in os.listdir(input_img_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

    if not input_files:
        print("Input_Image folder is empty. Place your image in the folder and rerun")
        sys.exit()
    elif len(input_files) > 1:
        print("Multiple images found in Input_Image folder. Ensure only one image is present")
        sys.exit()

    input_img = Image.open(os.path.join(input_img_path, input_files[0])).convert('RGB')
    print(f"Input image loaded: {input_files[0]}")
    return input_img


