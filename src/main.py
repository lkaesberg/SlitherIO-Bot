import time
from io import StringIO

import PIL
import numpy
from PIL import Image

from src.game.slither_game import SlitherGame

if __name__ == '__main__':
    height = 500
    width = 500
    game = SlitherGame()
    game.start_game("Test", width, height)
    while not game.is_game_running():
        time.sleep(0.01)
    now = time.time()
    im = game.get_screenshot()

    print(im.size)
    print(time.time() - now)
    im.show()
