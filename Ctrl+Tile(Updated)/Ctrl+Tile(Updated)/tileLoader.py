from PIL import Image
import os, csv
import numpy as np
import pandas as pd
from scipy.spatial import KDTree
from config import csv3_path

def extract_rgb_patch(img, grid_size=5):
    patch = img.resize((grid_size, grid_size)).convert('RGB')
    return (np.array(patch).astype(np.float32) / 255.0).flatten()

def extract_gray_patch(img, grid_size=5):
    patch = img.resize((grid_size, grid_size)).convert('L')
    return (np.array(patch).astype(np.float32) / 255.0).flatten()

def extract_histogram(img, bins=16):
    arr = np.array(img)
    hist = []
    for ch in range(3):  # R, G, B
        h, _ = np.histogram(arr[..., ch], bins=bins, range=(0, 256))
        hist.extend(h)
    hist = np.array(hist).astype(np.float32)
    return hist / (np.sum(hist) + 1e-10)


def check_feature_shape(name, features):
    if not features:
        raise ValueError(f"{name} feature list is empty.")
    first_len = len(features[0])
    for i, feat in enumerate(features):
        if len(feat) != first_len:
            raise ValueError(f"Inconsistent length in {name} feature at index {i}: got {len(feat)}, expected {first_len}")


# Function populates the lists
def appendTo(tilePath, tiles,  ssim_features, mse_features, hist_features):
  try:
    img = Image.open(tilePath)
    ssim_feat = extract_rgb_patch(img, grid_size=5)
    mse_feat = extract_gray_patch(img, grid_size=5)
    hist_feat = extract_histogram(img)

    # Note, .append() in a function will affect the original lists
    # But the assignment operator (=) will not
    tiles.append(img)
    ssim_features.append(ssim_feat)
    mse_features.append(mse_feat)
    hist_features.append(hist_feat)

    check_feature_shape("SSIM", ssim_features)
    check_feature_shape("MSE", mse_features)
    check_feature_shape("HIST", hist_features)

  except Exception as e:
    print(f" Skipping invalid image: {tilePath} — {e}")

  pass


# Main function
def load_tiles_from_csv(tile_directory, user_directory, dataset_option, csv_path):
    tiles = []
    ssim_features, mse_features, hist_features = [], [], []

    # Doesn't include header row
    datasetCSV = pd.read_csv(csv_path)

    # Load relevant tiles & get their info
    for opt in dataset_option:

        if opt == 'U' and user_directory is not None:

            print(f"loading U tiles from: {csv3_path}")
            print('                      ' + user_directory)
            with open(csv3_path, 'r') as ufile:
                reader = csv.reader(ufile)

                for row in reader:
                    tile_path = os.path.join(user_directory, row[0])
                    appendTo(tile_path, tiles, ssim_features, mse_features, hist_features)

        if opt == 'P':

            print(f"loading P tiles from: {csv_path}")
            print('                      ' + tile_directory)
            for i in range(0, 500):
                name = datasetCSV.iloc[i, 0]
                tile_path = os.path.join(tile_directory, name)
                appendTo(tile_path, tiles, ssim_features, mse_features, hist_features)

        if opt == 'A':

            print(f"loading A tiles from: {csv_path}")
            print('                      ' + tile_directory)
            for i in range(1500, 2000):
                name = datasetCSV.iloc[i, 0]
                tile_path = os.path.join(tile_directory, name)
                appendTo(tile_path, tiles, ssim_features, mse_features, hist_features)

        if opt == 'L':

            print(f"loading L tiles from: {csv_path}")
            print('                      ' + tile_directory)
            for i in range(1000, 1500):
                name = datasetCSV.iloc[i, 0]
                tile_path = os.path.join(tile_directory, name)
                appendTo(tile_path, tiles, ssim_features, mse_features, hist_features)

        if opt == 'M':

            print(f"loading M tiles from: {csv_path}")
            print('                      ' + tile_directory)
            for i in range(500, 1000):
                name = datasetCSV.iloc[i, 0]
                tile_path = os.path.join(tile_directory, name)
                appendTo(tile_path, tiles, ssim_features, mse_features, hist_features)
    
    print(f"Loaded {len(tiles)} tile images for matching\n")

    return {
        "ssim": (tiles, KDTree(ssim_features), np.array(ssim_features)),
        "mse":  (tiles, KDTree(mse_features), np.array(mse_features)),
        "hist": (tiles, KDTree(hist_features), np.array(hist_features)),
    }
