import os
import requests
import shutil
import numpy as np
import re
from PIL import Image
from dotenv import load_dotenv
from service.media_assets.colourScheme import colour_waveHight_map_at_40_quant
from service.media_assets.coordinates import location_pixel_coordinate_map

class MeteoGifService:
    def __init__(self):
        from repository.repository_gif import GifDataRepository
        from repository.repository_gif import DailyGifReadingRepository
        from service.service_utils import ServiceUtils
        self.service_utils = ServiceUtils()
        self.gif_data_repo = GifDataRepository()
        self.daily_gif_data_repo  = DailyGifReadingRepository()
        load_dotenv()
        self.gif_url = os.getenv("gif_url")
        self.gif_directory = os.path.join(os.getcwd(),  "service", "media_assets", "gifs")
        self.frames_directory = os.path.join(os.getcwd(),  "service", "media_assets", "frames")
        self.frames_edited_directory = os.path.join(os.getcwd(), "service", "media_assets", "framesEdited")
        self.coordinates = location_pixel_coordinate_map
        self.colour_waveHight_map = colour_waveHight_map_at_40_quant
    
    def insert_gif_data(self, wave_read, wave_unit_id, date, location_id):
        return self.gif_data_repo.insert_data(wave_read, wave_unit_id, date, location_id)

    def get_all_gif_data(self):
        return self.gif_data_repo.read_all_data()

    def delete_all_gif_data(self):
        return self.gif_data_repo.delete_all_data()

    def insert_daily_gif_reading(self, daily_wave_max=None, daily_wave_min=None, daily_wave_avg=None,
                                 wave_unit_id=None, date=None, location_id=None):
        return self.daily_gif_data_repo .insert_data(daily_wave_max, daily_wave_min, daily_wave_avg, wave_unit_id,
                                                       date, location_id)

    def get_all_daily_gif_readings(self):
        return self.daily_gif_data_repo .read_all_data()

    def delete_all_daily_gif_readings(self):
        return self.daily_gif_data_repo .delete_all_data()

    def fetch_gif_data(self):
        self._download_gif(self.gif_url, self.gif_directory)
        self._extract_gif_frames(self.gif_directory, self.frames_directory)
        self._quantize_colors_in_directory(self.frames_directory, self.frames_edited_directory, 40)
        data = self._analyze_image(self.frames_edited_directory, self.colour_waveHight_map, self.coordinates)
        self._delete_all_files(self.gif_directory, self.frames_directory, self.frames_edited_directory)
        return data
    
    def _download_gif(self, gif_url, download_location):
        
        gif_path = os.path.join(download_location, 'downloaded.gif')
        response = requests.get(gif_url)

        if response.status_code == 200:
            with open(gif_path, 'wb') as gif_file:
                gif_file.write(response.content)
            return gif_path
        else:
            print(f'Failed to download GIF. Status code: {response.status_code}')
            self.service_utils.insert_data_fetching_log(f'Failed to download GIF. Status code: {response.status_code}')
            return None

    def _extract_gif_frames(self, folder_path, frame_folder):
        if not os.path.exists(folder_path):
            print(f"Folder GIF {folder_path} does not exist.")
            return

        gif_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.gif')]
        if not gif_files:
            print("No GIF files found in the folder.")
            return

        gif_path = os.path.join(folder_path, gif_files[0])

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

    def _analyze_image(self, source_path, color_dict, location_coordinate_map):
        results = [] 
        frame_pattern = re.compile(r"quantized_frame_(\d+)\.\w+")

        for image_file in os.listdir(source_path):
            match = frame_pattern.match(image_file)
            if not match:
                print(f"Skipping file {image_file} as it does not match the expected pattern.")
                continue

            frame_id = int(match.group(1)) 
            image_path = os.path.join(source_path, image_file)
            image = Image.open(image_path)

            if image.mode != 'RGB':
                image = image.convert('RGB')

            image_array = np.array(image)

            for location, coords in location_coordinate_map.items():
                if not isinstance(coords, tuple) or len(coords) != 2:
                    continue

                x, y = coords
                found = False

                while not found and x < image_array.shape[1]:
                    try:
                        pixel_rgb = tuple(image_array[y, x])
                        for index, colors in color_dict.items():
                            if list(pixel_rgb) in colors:
                                results.append({
                                    "id": frame_id,
                                    "location": location,
                                    "index": float(index)
                                })
                                found = True
                                break

                        if not found:
                            x += 1

                    except IndexError:
                        break

                if not found:
                    results.append({
                        "id": frame_id,
                        "location": location,
                        "index": None 
                    })

        return results


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

