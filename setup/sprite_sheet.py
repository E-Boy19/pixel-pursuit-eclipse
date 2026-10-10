from os import path

from pygame import image, Rect, transform


class SpriteSheet:
    def __init__(self, filename, frame_size):
        self.sprite_sheet = image.load(path.join(filename))
        self.sprite_sheet = self.sprite_sheet.convert_alpha()
        self.frame_width = frame_size[0]
        self.frame_height = frame_size[1]

    def get_frame(self, x, y, to_size=None):
        rect = Rect(x, y, self.frame_width, self.frame_height)
        frame = self.sprite_sheet.subsurface(rect)
        if to_size:
            frame = transform.scale(frame, to_size)
        return frame
