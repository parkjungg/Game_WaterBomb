import os
from PIL import Image

class Item:
    def __init__(self, row, col, item_type, tile_size, sprite_folder):
        self.row = row
        self.col = col
        self.item_type = item_type
        self.sprite_folder = sprite_folder
        self.tile_size = tile_size

        # 아이템 이미지 로드
        self.image = Image.open(
            os.path.join(sprite_folder, f"{item_type}.png")
        ).resize((tile_size, tile_size))

    def draw(self, canvas):
        canvas.paste(self.image, (self.col * self.tile_size, self.row * self.tile_size))