# imports
from pathlib import Path

# module paths
DIRECTORY : Path = Path.cwd()
SOURCE : Path = DIRECTORY /'src'

ASSETS : Path = DIRECTORY /'assets'
TEMPORARY : Path = DIRECTORY /'temp'
DATA : Path = DIRECTORY /'data'

BIN : Path = DIRECTORY /'bin'

# ffmpeg .exe files
FFMPEG : Path = BIN /'video' /'bin' /'ffmpeg.exe'
FFPLAY : Path = BIN /'video' /'bin' /'ffplay.exe'
FFPROBE : Path = BIN /'video' /'bin' /'ffprobe.exe'