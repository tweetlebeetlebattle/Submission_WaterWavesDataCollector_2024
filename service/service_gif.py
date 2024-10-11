import os
import requests
import shutil
import numpy as np
from PIL import Image
from dotenv import load_dotenv
from media_assets.colourScheme import colour_waveHight_map_at_40_quant
from media_assets.coordinates import location_pixel_coordinate_map

class MeteoGifService:
    def __init__(self):
        load_dotenv()
        self.gif_url = os.getenv("gif_url")
        self.gif_directory = os.getenv("gifSource")
        self.frames_directory = os.getenv("framesDirectory")
        self.frames_edited_directory = os.getenv("framesEditedDirectory")
        self.coordinates = location_pixel_coordinate_map
        self.colour_waveHight_map = colour_waveHight_map_at_40_quant

    def fetch_gif_data(self):
        """Public method to handle the entire GIF fetching, processing, and analysis workflow."""
        self._download_gif(self.gif_url, self.gif_directory)
        self._extract_gif_frames(self.gif_directory, self.frames_directory)
        self._quantize_colors_in_directory(self.frames_directory, self.frames_edited_directory, 40)
        self._analyze_image(self.frames_edited_directory, self.colour_waveHight_map, self.coordinates)
        self._delete_all_files(self.gif_directory, self.frames_directory, self.frames_edited_directory)

    def _download_gif(self, gif_url, download_location):
        gif_path = os.path.join(download_location, 'downloaded.gif')
        response = requests.get(gif_url)

        with open(gif_path, 'wb') as gif_file:
            gif_file.write(response.content)

        print(f'GIF downloaded and saved to {gif_path}')
        return gif_path

    def _extract_gif_frames(self, folder_path, frame_folder):
        if not os.path.exists(folder_path):
            print(f"Folder GIF {folder_path} does not exist.")
            return

        gif_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.gif')]
        if not gif_files:
            print("No GIF files found in the folder.")
            return

        gif_path = os.path.join(folder_path, gif_files[0])
        print(f"Extracting frames from {gif_path}")

        if not os.path.exists(frame_folder):
            print(f"Folder FRAMES {frame_folder} does not exist.")
            return

        try:
            gif = Image.open(gif_path)
            frame_number = 0
            while True:
                try:
                    gif.seek(frame_number)
                    frame = gif.copy()
                    frame.save(os.path.join(frame_folder, f'frame_{frame_number}.png'))
                    print(f"Frame {frame_number} saved.")
                    frame_number += 1
                except EOFError:
                    print("All frames extracted.")
                    break
        except Exception as e:
            print(f"Error extracting frames: {e}")

    def _quantize_colors_in_directory(self, source_path, destination_path, quantization_level):
        if not os.path.exists(destination_path):
            os.makedirs(destination_path)
            print(f"Created destination directory: {destination_path}")

        def quantize_color(rgb, levels):
            return tuple((value // levels) * levels for value in rgb)

        for filename in os.listdir(source_path):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(source_path, filename)
                print(f"Processing image: {image_path}")

                image = Image.open(image_path)
                if image.mode != 'RGB':
                    image = image.convert('RGB')

                image_array = np.array(image)
                quantized_image_array = np.zeros_like(image_array)
                color_dict = {}

                height, width, _ = image_array.shape
                for y in range(height):
                    for x in range(width):
                        pixel_value = tuple(image_array[y, x])
                        quantized_color = quantize_color(pixel_value, quantization_level)
                        quantized_image_array[y, x] = quantized_color

                        if quantized_color not in color_dict:
                            color_dict[quantized_color] = 1
                        else:
                            color_dict[quantized_color] += 1

                quantized_image = Image.fromarray(quantized_image_array.astype('uint8'), 'RGB')
                output_image_path = os.path.join(destination_path, f'quantized_{filename}')
                quantized_image.save(output_image_path)
                print(f"Quantized image saved as {output_image_path}")
                print(f"Total unique colors after quantization: {len(color_dict)}")
                print("Sample of unique colors (first 10):", list(color_dict.items())[:10])
                print()

    def _analyze_image(self, source_path, color_dict, location_coordinate_map):
        for image_file in os.listdir(source_path):
            if image_file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                image_path = os.path.join(source_path, image_file)
                image = Image.open(image_path)

                if image.mode != 'RGB':
                    image = image.convert('RGB')

                image_array = np.array(image)
                print(f"Analyzing image: {image_file}")

                for location, coords in location_coordinate_map.items():
                    print(f"Location: {location}, Initial Coordinates: {coords}")

                    if not isinstance(coords, tuple) or len(coords) != 2:
                        print(f"Error: Invalid coordinates for {location}. Expected a tuple of (x, y), got {coords}")
                        continue

                    x, y = coords
                    found = False

                    while not found and x < image_array.shape[1]:
                        try:
                            pixel_rgb = tuple(image_array[y, x])
                            for index, colors in color_dict.items():
                                if list(pixel_rgb) in colors:
                                    print(f"{location} ({x}, {y}): Found index {index}")
                                    found = True
                                    break

                            if not found:
                                print(f"{location} ({x}, {y}): Not found in dictionary. RGB value: {pixel_rgb}")
                                x += 1

                        except IndexError:
                            print(f"{location} ({x}, {y}): Coordinates are out of bounds for this image.")
                            break

                    if not found:
                        print(f"{location}: No match found in the entire row for the starting y-coordinate {y}.")

    def _delete_all_files(self, *directories):
        for directory in directories:
            if os.path.exists(directory):
                print(f"Deleting all files in directory: {directory}")
                for filename in os.listdir(directory):
                    file_path = os.path.join(directory, filename)
                    try:
                        if os.path.isfile(file_path) or os.path.islink(file_path):
                            os.unlink(file_path)
                            print(f"Deleted file: {file_path}")
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                            print(f"Deleted directory and its contents: {file_path}")
                    except Exception as e:
                        print(f"Failed to delete {file_path}. Reason: {e}")
            else:
                print(f"Directory {directory} does not exist.")

# Usage
gif_service = GifProcessingService()
gif_service.fetch_gif_data()
