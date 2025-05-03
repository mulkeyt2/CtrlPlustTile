# === Restored config.py (Updated for tile CSVs) ===

import os

# Set your base project directory
project_path = os.path.join(os.getcwd())

# Dataset Paths
base_path = os.path.join(project_path, 'Images_Dataset')
tilePath = os.path.join(base_path, 'Tiled_Images')
x5Path = os.path.join(tilePath, '5x5_Tiles')
x10Path = os.path.join(tilePath, '10x10_Tiles')
x15Path = os.path.join(tilePath, '15x15_Tiles')
x20Path = os.path.join(tilePath, '20x20_Tiles')

# CSV paths (original + generated per tile size)
csv_path = os.path.join(base_path, 'image_labels.csv')
tile_csv_5 = os.path.join(tilePath, 'tile_data_5.csv')
tile_csv_10 = os.path.join(tilePath, 'tile_data_10.csv')
tile_csv_15 = os.path.join(tilePath, 'tile_data_15.csv')
tile_csv_20 = os.path.join(tilePath, 'tile_data_20.csv')

# User Uploads
uploadPath = os.path.join(project_path, 'User_Uploaded')
newPath = os.path.join(uploadPath, 'New_Uploads')
oldPath = os.path.join(uploadPath, 'Old_Uploads')
squareUserPath = os.path.join(uploadPath, 'Square_Images')
u5Path = os.path.join(uploadPath, 'Tiled_Images', '5x5_Tiles')
u10Path = os.path.join(uploadPath, 'Tiled_Images', '10x10_Tiles')
u15Path = os.path.join(uploadPath, 'Tiled_Images', '15x15_Tiles')
u20Path = os.path.join(uploadPath, 'Tiled_Images', '20x20_Tiles')

# Tile CSVs for user tiles (optional, not required by default)
tile_user_csv_5 = os.path.join(u5Path, 'tile_data_user_5.csv')
tile_user_csv_10 = os.path.join(u10Path, 'tile_data_user_10.csv')
tile_user_csv_15 = os.path.join(u15Path, 'tile_data_user_15.csv')
tile_user_csv_20 = os.path.join(u20Path, 'tile_data_user_20.csv')

csv2_path = os.path.join(uploadPath, 'new_user_image_labels.csv')
csv3_path = os.path.join(uploadPath, 'all_user_image_labels.csv')

# Centralized configuration for shared runtime state
outputOption = None
tileSize = None
datasetOption = None
Tiled_Images = None
User_Tiled_Images = None
