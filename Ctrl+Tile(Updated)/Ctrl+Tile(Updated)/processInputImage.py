from PIL import Image
import os
import sys

# Load and split the input image into tiles

# Function splits the input image into tiles of the specified size
def split_image(image, tile_size):
    tiles = []
    rows, cols = image.size[1] // tile_size[1], image.size[0] // tile_size[0]

    for r in range(rows):
        for c in range(cols):
            tile = image.crop((
                c * tile_size[0],
                r * tile_size[1],
                (c + 1) * tile_size[0],
                (r + 1) * tile_size[1]
            ))
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

