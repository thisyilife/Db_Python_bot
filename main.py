import cv2
import numpy as np

from vision import Vision as vis
from mouseControl import Controller as con
from game import Game as game



v = vis()
c = con()
g = game(v,c) 
g.run(state = 'Dices')
#g.test() 
