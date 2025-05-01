import os
import csv
import sys
import shutil
from PIL import Image

from config import (
    tileSize, newPath, oldPath,
    u5Path, u10Path, u15Path, u20Path,
    csv2_path, csv3_path
)

'''
- Performs pre-processing on the New_Uploads folder
  if specified by the user
- New uploads will automatically be moved into the
  Old_Uploads folder (already processed images)
- Takes a few minutes (depending on number of new uploads)
  for tiles to appear in folders

- Images taken by & uploaded from an iPhone may have their
  dimensions flipped (3,024 x 4,032 becomes 4,032 x 3,024).
  As a result, the square image may be rotated on its side.
  This is currently accounted for via dimensions-checking only
- Images with transparent backgrounds will become tiles with
  black backgrounds

'''

# Function squares the user uploaded images & resizes them as tiles
def squareAndTileUser():

  # Create Tiled_Images subfolders
  os.makedirs(u5Path, exist_ok=True)
  os.makedirs(u10Path, exist_ok=True)
  os.makedirs(u15Path, exist_ok=True)
  os.makedirs(u20Path, exist_ok=True)

  print('tiling user uploads...')

  # Crop & resize each image from the CSV
  with open(csv2_path, 'r') as imagesFile:
    header = next(imagesFile)
    imageReader = csv.reader(imagesFile)

    for row in imageReader:
      input_path = os.path.join(newPath, row[0])

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

      # Read bullet point 4 in the comment block above
      # Rotate square image 270 degrees counterclockwise
      if width == 4032 and height == 3024:
        square_img = square_img.rotate(270)

      # Resize the square image into 5x5, 10x10, 15x15, & 20x20 tiles
      # while trying to retain quality
      img1 = square_img.resize((5,5), Image.LANCZOS)
      img2 = square_img.resize((10,10), Image.LANCZOS)
      img3 = square_img.resize((15,15), Image.LANCZOS)
      img4 = square_img.resize((20,20), Image.LANCZOS)

      # Correctly construct the paths for saving tiled images
      img1Image = os.path.join(u5Path, row[0])
      img2Image = os.path.join(u10Path, row[0])
      img3Image = os.path.join(u15Path, row[0])
      img4Image = os.path.join(u20Path, row[0])

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

  print('tiles complete')

  pass


# Function performs pre-processing for user uploaded images
def userUploaded():

  newFolder = os.listdir(newPath)
  oldFolder = os.listdir(oldPath)

  # If both folders are empty, prompt the user
  if not newFolder and not oldFolder:
    print('There are no images in the User_Uploaded folder')
    print('Upload some into the New_Uploads folder and rerun this section')
    sys.exit()

  # If there are no new uploads, use old uploads (already processed)
  if not newFolder:
    return

  print(f'\nfound {len(newFolder)} files in New_Uploads')

  # Create csv files
  os.makedirs(os.path.dirname(csv2_path), exist_ok=True)
  os.makedirs(os.path.dirname(csv3_path), exist_ok=True)

  # Now write to new uploads .csv
  # And append to all uploads .csv
  with open(csv2_path, 'w', newline='') as f1, open(csv3_path, 'a') as f2:
    writer = csv.writer(f1)
    writer2 = csv.writer(f2)
    writer.writerow(['filename', 'label'])

    for name in newFolder:
      if name.lower().endswith(('.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG')):
        writer.writerow([name, 'user_uploaded'])
        writer2.writerow([name, 'user_uploaded'])

  squareAndTileUser()

  for newFile in newFolder:
    shutil.move(os.path.join(newPath, newFile), oldPath)

  print(f"\nImages in New_Uploads folder have been moved to Old_Uploads folder\n")

