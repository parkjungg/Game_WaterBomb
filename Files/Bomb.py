from PIL import Image
import os

class Bomb:
    """폭탄 클래스"""
    def __init__(self, row, col, tile_size, sprite_folder, map_data):
        self.row = row
        self.col = col
        self.x = col * tile_size + tile_size // 2
        self.y = row * tile_size + tile_size // 2
        self.tile_size = tile_size
        self.timer = 1.5  # 폭발까지의 시간 (초)
        self.effect_duration = 0.5  # 폭발 이펙트 지속 시간 (초)
        self.exploded = False  # 폭발 여부
        self.sprite_folder = os.path.abspath(sprite_folder)

        tile_type = map_data[row][col]
        if tile_type == "road":
            bomb_image_name = "bomb0.png"
        elif tile_type == "grass":
            bomb_image_name = "bomb1.png"
        
        # 폭탄 이미지와 폭발 이펙트 이미지 로드
        self.bomb_image = Image.open(os.path.join(sprite_folder, bomb_image_name)).resize((tile_size, tile_size))
        self.effect_image = Image.open(os.path.join(sprite_folder, "boomeffect.png")).resize((tile_size, tile_size))

    def get_explosion_range(self, map_data, power):
        """폭발 범위 좌표 리스트 반환 (중앙 + 상하좌우)"""
        directions = [(0, 0)]  # 중앙 포함
        for i in range(1, power + 1):
            directions.extend([(-i, 0), (i, 0), (0, -i), (0, i)])  # 상하좌우 power 범위
        explosion_range = []
        for dr, dc in directions:
            r, c = self.row + dr, self.col + dc
            if 0 <= r < len(map_data) and 0 <= c < len(map_data[0]):  # 맵 범위 확인
                explosion_range.append((r, c))
        return explosion_range

    def draw(self, canvas, map_data, explosion_power):
        """폭탄 또는 폭발 이펙트 그리기"""
        if not self.exploded:
            # 폭탄 표시
            canvas.paste(self.bomb_image, (self.col * self.tile_size, self.row * self.tile_size))
        else:
            # 폭발 이펙트 표시
            for r, c in self.get_explosion_range(map_data, explosion_power):
                canvas.paste(self.effect_image, (c * self.tile_size, r * self.tile_size))