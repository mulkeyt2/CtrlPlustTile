# === Restored createCSV.py ===

import os
import csv
from config import base_path, csv_path

# Automatically scan all folders under base_path (Images_Dataset folder)
# and index the images via their filename & category in a CSV file

print("Folders found in Images_Dataset:\n")

output_rows = []

for folder in os.listdir(base_path):
    full_path = os.path.join(base_path, folder)
    if os.path.isfile(full_path):
        print(f"  file '{folder}'\n")
        continue
    
    # For rerunning purposes (if needed)
    if folder == 'Tiled_Images':
        print(f"  skipping {folder}\n")
        continue

    print(f"  scanning: {folder}: folder -> label: {folder.lower()}  ")

    image_files = [f for f in os.listdir(full_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    print(f"  found {len(image_files)} files in {folder}\n")

    for img_file in image_files:
        relative_path = os.path.join(folder, img_file).replace("\\", "/")
        label = folder.lower()
        output_rows.append([relative_path, label])

# Create CSV file
os.makedirs(os.path.dirname(csv_path), exist_ok=True)

# Write to CSV file
with open(csv_path, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['filename', 'label'])
    writer.writerows(output_rows)

print(f"Wrote {len(output_rows)} rows to {csv_path}")
