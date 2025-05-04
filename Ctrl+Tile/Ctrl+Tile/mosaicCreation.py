import os
import subprocess
import platform
from datetime import datetime
import numpy as np
from PIL import Image
from tqdm import tqdm
from skimage.color import rgb2gray
from skimage.metrics import structural_similarity as ssim
from tileLoader import load_tiles_from_csv, extract_rgb_patch, extract_gray_patch, extract_histogram
from collections import defaultdict as DefaultDict


RESIZE_DIMS = (50, 50)

def calculate_ssim(image1, image2):
    arr1 = rgb2gray(np.array(image1.resize(RESIZE_DIMS)).astype(np.float32) / 255.0)
    arr2 = rgb2gray(np.array(image2.resize(RESIZE_DIMS)).astype(np.float32) / 255.0)
    score, _ = ssim(arr1, arr2, data_range=1.0, full=True)
    return score

def calculate_mse(image1, image2):
    arr1 = np.array(image1.resize(RESIZE_DIMS)).astype(np.float32)
    arr2 = np.array(image2.resize(RESIZE_DIMS)).astype(np.float32)
    return np.mean((arr1 - arr2) ** 2)

def calculate_histogram_dist(image1, image2, bins=16):
    hist1 = extract_histogram(image1, bins)
    hist2 = extract_histogram(image2, bins)
    return np.linalg.norm(hist1 - hist2)

def find_best_match(segment, tiles, tree, features, method, top_n=10, usage_counts=None): #, max_usage=300
    if method == 'ssim':
        query_feat = extract_rgb_patch(segment, grid_size=5)
    elif method == 'mse':
        query_feat = extract_gray_patch(segment, grid_size=5)
    elif method == 'hist':
        query_feat = extract_histogram(segment)
    else:
        raise ValueError(f"Unknown method: {method}")

    _, indices = tree.query([query_feat], k=top_n)

    best_score = float('inf') if method in ['mse', 'hist'] else -1
    best_tile = None
    best_index = -1

    for i in indices[0]:
        #if usage_counts and usage_counts[i] >= max_usage:
           # continue

        tile_img = tiles[i]
        if method == 'ssim':
            score = calculate_ssim(segment, tile_img)
            if score > best_score:
                best_score = score
                best_tile = tile_img
                best_index = i
        elif method == 'mse':
            score = calculate_mse(segment, tile_img)
            if score < best_score:
                best_score = score
                best_tile = tile_img
                best_index = i
        elif method == 'hist':
            score = calculate_histogram_dist(segment, tile_img)
            if score < best_score:
                best_score = score
                best_tile = tile_img
                best_index = i

    if best_tile and usage_counts is not None:
        usage_counts[best_index] += 1

    return best_tile, best_score

def construct_mosaic_from_method(input_tiles, tiles, tree, features, method): #, max_usage=300
    matched_tiles = []
    usage_counts = DefaultDict(int)
    for tile in tqdm(input_tiles, desc=f"Matching tiles ({method.upper()})"):
        match, _ = find_best_match(tile, tiles, tree, features, method=method, usage_counts=usage_counts) #, max_usage=max_usage
        if match is None:
            least_used_index = min(range(len(tiles)), key=lambda i: usage_counts[i])
            match = tiles[least_used_index]
            usage_counts[least_used_index] += 1
        matched_tiles.append(match)
    return matched_tiles

def build_mosaic(tiles, tile_size, rows, cols):
    mosaic = Image.new('RGB', (cols * tile_size[0], rows * tile_size[1]))
    for i, tile in enumerate(tiles):
        r = i // cols
        c = i % cols
        mosaic.paste(tile, (c * tile_size[0], r * tile_size[1]))
    return mosaic

def build_all_mosaics(input_tiles, tile_data, tile_size, rows, cols):
    mosaics = []
    for method in ['ssim', 'mse', 'hist']:
        tiles, tree, features = tile_data[method]
        matched = construct_mosaic_from_method(input_tiles, tiles, tree, features, method) #, max_usage=300
        mosaic = build_mosaic(matched, tile_size, rows, cols)
        mosaics.append((method, mosaic))
    return mosaics

def show_all_mosaics(mosaics, tile_size=(50, 50), save_dir="Mosaic_Results"):
    print('')
    os.makedirs(save_dir, exist_ok=True)
    for method, mosaic in mosaics:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        filename = f"{method.upper()}_mosaic_{tile_size[0]}x{tile_size[1]}_{timestamp}.png"
        filepath = os.path.join(save_dir, filename)
        mosaic.save(filepath)
        print(f"Saved: {filepath}")
        if platform.system() == 'Windows':
            os.system(f'start "" "{filepath}"')

def run_mosaic(tile_directory, user_directory, dataset_option, csv_path, output_option):
    try:
        print("Calling load_tiles...")
        tile_data = load_tiles_from_csv(tile_directory, user_directory, dataset_option, csv_path)

        if output_option == 'S':
            print("Loading tiles for SSIM, MSE, and HIST")
        else:
            print("Loading tiles")
        # tile_data is a dictionary that contains
        #   "ssim": (tiles, KDTree(ssim_features), np.array(ssim_features))
        #   "mse":  (tiles, KDTree(mse_features), np.array(mse_features))
        #   "hist": (tiles, KDTree(hist_features), np.array(hist_features))
        return tile_data
    except Exception as e:
        print("Error occurred while loading tiles:", e)
        return None