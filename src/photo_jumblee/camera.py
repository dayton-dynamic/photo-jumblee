
import numpy as np
import cv2 as cv
import random
from dataclasses import dataclass
from matrix import chop, fuse, reorder_sequence

@dataclass
class Jumbler:
    n_horiz = 3 
    n_vert = 3 
    width_pixels = 640
    height_pixels = 480

    def __post_init__(self):
        self.redo_grid()

    def redo_grid(self):
        self.original_order = list(range(self.n_horiz * self.n_vert))
        self.display_order = self.original_order[:]
        self.piece_width_px = int(self.width_pixels / self.n_horiz)
        self.piece_height_px = int(self.height_pixels / self.n_vert)
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.display_order)

    def unshuffle(self):
        self.display_order = self.original_order[:]

    def reverse(self):
        self.display_order = self.original_order[:]
        self.display_order.reverse()

    def jumbled(self, frame):
        pieces = list(chop(frame, self.piece_width_px, self.piece_height_px))
        pieces = reorder_sequence(pieces, self.display_order)
        return fuse(pieces, self.n_horiz) 


def main():
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    jumbler = Jumbler()
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
            
        frame = jumbler.jumbled(frame)

        # Display the resulting frame
        cv.imshow('frame', frame)
        keypress = cv.waitKey(1)
        if keypress == ord('q'):
            break
        elif keypress == ord('s'):
            jumbler.shuffle()
        elif keypress == ord('o'):
            jumbler.unshuffle()
        elif keypress == ord('r'):
            jumbler.reverse()
        elif keypress == ord('+'):
            jumbler.n_horiz += 1
            jumbler.redo_grid()
        elif keypress == ord('-'):
            jumbler.n_horiz = max(jumbler.n_horiz - 1, 1)
            jumbler.redo_grid()


    # When everything done, release the capture
    cap.release()
    cv.destroyAllWindows()

if __name__ == '__main__':
    main()