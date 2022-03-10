"""
this is our main Driver File.
Handle user input
current state GameState Object

"""
import pygame as p
import os
import ChessEngine

dir_path = os.path.dirname(os.path.realpath(__file__))
WIDTH = HIGHT = 512 # 400
DIMENSION = 8 # dimensions of chess is 8*8
SQ_size = HIGHT // DIMENSION
BOARD_COLOR = (p.Color('white'), p.Color('gray'))
MAX_FPS = 15
IMAGES = {}

def main():
    pass


if __name__ == '__main__':
    main()

