import os
import csv
from PIL import Image, ImageOps

from config import (
    base_path, x5Path, x10Path, x15Path, x20Path, csv_path
)

# Create Tiled_Images subfolders
os.makedirs(os.path.join(x5Path, 'Portraits_People_and_Animals'), exist_ok=True)
os.makedirs(os.path.join(x5Path, 'Materials_Buildings_Objects_Food'), exist_ok=True)
os.makedirs(os.path.join(x5Path, 'Landscapes_Nature'), exist_ok=True)
os.makedirs(os.path.join(x5Path, 'Abstract_Art_Patterns_Colors'), exist_ok=True)

os.makedirs(os.path.join(x10Path, 'Portraits_People_and_Animals'), exist_ok=True)
os.makedirs(os.path.join(x10Path, 'Materials_Buildings_Objects_Food'), exist_ok=True)
os.makedirs(os.path.join(x10Path, 'Landscapes_Nature'), exist_ok=True)
os.makedirs(os.path.join(x10Path, 'Abstract_Art_Patterns_Colors'), exist_ok=True)

os.makedirs(os.path.join(x15Path, 'Portraits_People_and_Animals'), exist_ok=True)
os.makedirs(os.path.join(x15Path, 'Materials_Buildings_Objects_Food'), exist_ok=True)
os.makedirs(os.path.join(x15Path, 'Landscapes_Nature'), exist_ok=True)
os.makedirs(os.path.join(x15Path, 'Abstract_Art_Patterns_Colors'), exist_ok=True)

os.makedirs(os.path.join(x20Path, 'Portraits_People_and_Animals'), exist_ok=True)
os.makedirs(os.path.join(x20Path, 'Materials_Buildings_Objects_Food'), exist_ok=True)
os.makedirs(os.path.join(x20Path, 'Landscapes_Nature'), exist_ok=True)
os.makedirs(os.path.join(x20Path, 'Abstract_Art_Patterns_Colors'), exist_ok=True)

# Define category folders
categories = [
    'Portraits_People_and_Animals',
    'Materials_Buildings_Objects_Food',
    'Landscapes_Nature',
    'Abstract_Art_Patterns_Colors'
]

# Process and crop each image from the CSV
# into the largest square image possible (at the center)
with open(csv_path, 'r') as imagesFile:
    header = next(imagesFile)
    imageReader = csv.reader(imagesFile)

    for row in imageReader:
        input_path = os.path.join(base_path, row[0])

        try:
            img = Image.open(input_path).convert('RGB')
        except Exception as e:
            print(f"Could not open {row[0]}: {e}")
            continue

        width, height = img.size
        side = min(width, height)

        # Center crop
        left = (width - side) // 2
        top = (height - side) // 2
        right = left + side
        bottom = top + side

        square_img = img.crop((left, top, right, bottom))

        # Resize the square image into 5x5, 10x10, 15x15, & 20x20 tiles
        # while trying to retain quality
        img1 = square_img.resize((5,5), Image.LANCZOS)
        img2 = square_img.resize((10,10), Image.LANCZOS)
        img3 = square_img.resize((15,15), Image.LANCZOS)
        img4 = square_img.resize((20,20), Image.LANCZOS)

        # Correctly construct the paths for saving tiled images
        img1Image = os.path.join(x5Path, row[0])
        img2Image = os.path.join(x10Path, row[0])
        img3Image = os.path.join(x15Path, row[0])
        img4Image = os.path.join(x20Path, row[0])

        # Ensure the files exist before saving the images
        os.makedirs(os.path.dirname(img1Image), exist_ok=True)
        os.makedirs(os.path.dirname(img2Image), exist_ok=True)
        os.makedirs(os.path.dirname(img3Image), exist_ok=True)
        os.makedirs(os.path.dirname(img4Image), exist_ok=True)

        # Save tiles as JPEG with low compression (higher quality)
        img1.save(img1Image, format='JPEG', quality=95, subsampling=0)
        img2.save(img2Image, format='JPEG', quality=95, subsampling=0)
        img3.save(img3Image, format='JPEG', quality=95, subsampling=0)
        img4.save(img4Image, format='JPEG', quality=95, subsampling=0)

print('tiling of dataset images complete\n')
