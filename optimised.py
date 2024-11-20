import os
import shutil
from PIL import Image

# Define the root directory
root_folder = '/Users/rabsun/Desktop/vj'  # Replace with your actual path

# Track processed files
processed_count = 0

# Walk through all directories and subdirectories
for dirpath, _, filenames in os.walk(root_folder):
    image_found = False  # Flag to check if any images are in the directory
    
    for filename in filenames:
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            img_path = os.path.join(dirpath, filename)
            print(f"Processing {img_path}...")  # Debug print
            
            # Set the flag to True since an image is found in this directory
            image_found = True

            # Create the optimized path only if there are images
            optimized_subfolder = os.path.join(dirpath, "optimized")
            os.makedirs(optimized_subfolder, exist_ok=True)
            optimized_path = os.path.join(optimized_subfolder, filename)
            
            try:
                with Image.open(img_path) as img:
                    if img.size[0] < 900:
                        # If image width is less than 700px, just copy it
                        shutil.copy(img_path, optimized_path)
                        print(f"Copied {filename} as it's already under 700px wide.")
                    else:
                        # Calculate the new height to maintain aspect ratio
                        width_percent = 900 / float(img.size[0])
                        new_height = int((float(img.size[1]) * width_percent))
                        
                        # Resize and optimize the image
                        img = img.resize((700, new_height), Image.LANCZOS)
                        
                        # Save the image in the "optimized" folder within the current subfolder
                        img.save(optimized_path, optimize=True, quality=85)
                        print(f"Resized and optimized {filename}.")
                    
                    processed_count += 1
            
            except Exception as e:
                print(f"Error processing {filename}: {e}")
                
    # Only create the "optimized" subfolder if at least one image was found
    if not image_found:
        print(f"No images found in {dirpath}, skipping 'optimized' folder creation.")

print(f"\nTotal images processed: {processed_count}")
