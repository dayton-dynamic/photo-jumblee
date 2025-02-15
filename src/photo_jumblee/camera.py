
import random
from dataclasses import dataclass

import cv2 as cv
from matrix import chop, fuse, reorder_sequence


MAX_HEIGHT_WID = 22 

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

    def shuffle(self):  # S
        random.shuffle(self.display_order)

    def unshuffle(self):  # O
        self.display_order = self.original_order[:]

    def reverse(self):  # R
        self.display_order.reverse()

    def advance(self):  # A
        self.display_order = [self.display_order[-1], *self.display_order[:-1]]

    def dupe(self):  # D
        center = len(self.display_order) // 2
        self.display_order = [center, ] * len(self.display_order)

    def more_cols(self):
        self.n_horiz += 1
        self.n_horiz = min(self.n_horiz, MAX_HEIGHT_WID)
        self.redo_grid()

    def fewer_cols(self):
        self.n_horiz = max(self.n_horiz - 1, 1)
        self.redo_grid()

    def more_rows(self):
        self.n_vert += 1
        self.n_vert = min(self.n_vert, MAX_HEIGHT_WID)
        self.redo_grid()

    def fewer_rows(self):
        self.n_vert = max(self.n_vert - 1, 1)
        self.redo_grid()

    def jumbled(self, frame):
        pieces = list(chop(frame, self.piece_width_px, self.piece_height_px))
        for (idx, piece) in enumerate(pieces):
            cv.putText(piece, str(idx), (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1.0, (255,255,255),2,cv.LINE_AA)
        pieces = reorder_sequence(pieces, self.display_order)
        return fuse(pieces, self.n_horiz) 

    RAW_MAPPING = {
        7: unshuffle,
        8: shuffle,
        # 9 handled in main()

        4: reverse,
        5: dupe,
        6: advance,

        1: fewer_cols,
        2: more_rows,
        3: more_cols,

        0: fewer_rows,
    }

    ORD_MAPPING = {ord(str(k)): v for k, v in RAW_MAPPING.items()}

    def dispatcher(self, keypress):
        # print(f"{keypress=}")
        # print(f"{self.ORD_MAPPING.get(keypress)=}")
        if func := self.ORD_MAPPING.get(keypress):
            func(self)


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
        else:
            jumbler.dispatcher(keypress)

    # When everything done, release the capture
    cap.release()
    cv.destroyAllWindows()

if __name__ == '__main__':
    main()