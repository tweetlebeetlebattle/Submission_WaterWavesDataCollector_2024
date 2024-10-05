from gifService import *
from dotenv import load_dotenv
from media_assets.colourScheme import colour_waveHight_map_at_40_quant
from media_assets.coordinates import location_pixel_coordinate_map
load_dotenv()
gifUrl = os.getenv("gif_url")
gifDirectory = os.getenv("gifSource")
framesDirectory = os.getenv("framesDirectory")
framesEditedDirectory = os.getenv("framesEditedDirectory")

coordinates = location_pixel_coordinate_map

def fetchGifData():
    download_gif(gifUrl, gifDirectory)
    extract_gif_frames(gifDirectory, framesDirectory)
    quantize_colors_in_directory(framesDirectory, framesEditedDirectory, 40)
    analyze_image(framesEditedDirectory, colour_waveHight_map_at_40_quant, coordinates)
    delete_all_files(gifDirectory, framesDirectory, framesEditedDirectory)