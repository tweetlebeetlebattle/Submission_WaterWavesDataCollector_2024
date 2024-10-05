from service.fetchNIMH_basic import *
from service.fetchNIMH_gif import *
from service.fetchStormGlass import *
def gather():
    fetchMeteoData()
    fetchGifData()
    fetchWeatherForAllLocations()
