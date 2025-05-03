import os
from datetime import datetime

def save_mosaic(output, project_path, input_name="final"):
    # Ask the user if they want to save the mosaic
    while True:
        save_output = input(f"\nDo you want to save the {input_name} mosaic to the Output_Mosaic(s) folder? Type Y or N: ").strip().lower()
        if save_output in ['y', 'n']:
            break
        print("Invalid option. Please type Y or N.")

    if save_output == 'y':
        # Ensure the output folder exists
        output_folder = os.path.join(project_path, "Output_Mosaic(s)")
        os.makedirs(output_folder, exist_ok=True)

        # Generate a unique file name
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(output_folder, f"{input_name}_{timestamp}.jpg")

        try:
            # Save the mosaic
            output.save(output_file, format="JPEG", quality=95)
            print(f"Mosaic saved successfully to: {output_file}")
        except Exception as e:
            print(f"Error saving mosaic: {e}")
    else:
        print("Mosaic not saved.")