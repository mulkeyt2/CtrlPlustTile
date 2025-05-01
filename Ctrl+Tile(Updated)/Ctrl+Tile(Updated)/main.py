# === Restored main.py ===

import os
import tqdm
import sys
from welcomePage import welcome_user
from processInputImage import load_input_image, split_image
#from tileLoader import load_tiles_from_csv
from mosaicCreation import build_all_mosaics, show_all_mosaics, run_mosaic
from saveOutput import save_mosaic
from userUploaded import userUploaded
import config

'''
Step 0: Pre-process the dataset images

    All 2000 images in the Images_Dataset folder have already been processed by the createCSV.py and squareAndResize.py files

    You, as the user, do not need to rerun those files

'''

# Please install tqdm, scikit-image, & pandas before running main!
# To do so, run the following in your terminal
# 'pip install tqdm; pip install scikit-image; pip install pandas'

def main():

    try:
        # Step 1: Welcome the user and get their options input
        output_option, dataset_option, tile_size, tile_directory = welcome_user()

        # Step 2: Handle user-uploaded images if selected
        if 'U' in dataset_option:
            userUploaded()

            if tile_size == (5, 5):
                user_directory = config.u5Path
            elif tile_size == (10, 10):
                user_directory = config.u10Path
            elif tile_size == (15, 15):
                user_directory = config.u15Path
            elif tile_size == (20, 20):
                user_directory = config.u20Path

        if output_option == 'S':
            # Step 3: Load the input image
            input_img = load_input_image(config.project_path)
            input_tiles, input_rows, input_cols = split_image(input_img, tile_size)

            # Step 4: Load dataset tiles using per-method KDTree system
            tile_data = run_mosaic(tile_directory, user_directory, dataset_option, config.csv_path)

            if tile_data is None:
                raise RuntimeError("Tile data failed to load.")

            # Step 5: Build all mosaics
            mosaics = build_all_mosaics(input_tiles, tile_data, tile_size, input_rows, input_cols)

            # Step 6: Display all mosaics
            show_all_mosaics(mosaics, tile_size=tile_size)

            # Step 7: Save the selected mosaic (e.g., first one)
            save_mosaic(mosaics[0][1], config.project_path, input_name="final_mosaic")
            
        elif output_option == 'W':
            print('W\n')
            # Placeholder

    except Exception as e:
        print(f"An error occurred in main: {e}")


if __name__ == "__main__":
    main()
    sys.exit(0)