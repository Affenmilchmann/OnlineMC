from os import path as ospath, mkdir

from discord.colour import Colour

DATA_FOLDER = ospath.join(ospath.dirname(__file__), "data/")
if not ospath.exists(DATA_FOLDER):
    try:
        mkdir(DATA_FOLDER)
    except OSError as e:
        print(f"Creation of the directory {DATA_FOLDER} failed")
        print(e)
    else:
        print(f"Successfully created the directory {DATA_FOLDER} ")

prefix = "mcon!"
refresh_emoji = "🔄"
default_embeds_colour = Colour.green()
API_PATH = "/mconline/"
DEFAULT_PORT = "11235"

owner_id = 360440725923430440