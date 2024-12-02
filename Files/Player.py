from PIL import Image
import random

class Player:
    """플레이어 클래스 정의"""
    def __init__(self, map_data, tile_size, sprite_folder):
        self.tile_size = tile_size
        self.map_data = map_data

        # 초기 위치 설정 (road나 grass 타일 중 랜덤 선택)
        self.row, self.col = self.get_random_spawn_location()

        # 현재 위치와 목표 위치
        self.x = self.col * self.tile_size + self.tile_size // 2
        self.y = self.row * self.tile_size + self.tile_size // 2
        self.target_x = self.x
        self.target_y = self.y

        # 플레이어 속성
        self.speed = 10 
        self.max_bombs = 1
        self.explosion_power = 1
        self.current_bombs = 0

        self.image = Image.open(f"{sprite_folder}/player.png").resize(
            (tile_size, tile_size), Image.ANTIALIAS)

    def get_random_spawn_location(self):
        """road 또는 grass 타일에서 랜덤 스폰 위치 가져오기"""
        valid_tiles = [(row_idx, col_idx) for row_idx, row in enumerate(self.map_data)
                       for col_idx, tile_type in enumerate(row) if tile_type in ["road", "grass"]]
        return random.choice(valid_tiles)

    def set_target(self, direction):
        """목표 위치를 설정"""
        new_row, new_col = self.row, self.col

        if direction == "up":
            new_row = max(self.row - 1, 0)
        elif direction == "down":
            new_row = min(self.row + 1, len(self.map_data) - 1)
        elif direction == "left":
            new_col = max(self.col - 1, 0)
        elif direction == "right":
            new_col = min(self.col + 1, len(self.map_data[0]) - 1)

        # 이동하려는 위치가 road나 grass인지 확인
        if self.map_data[new_row][new_col] in ["road", "grass"]:
            self.row, self.col = new_row, new_col
            self.target_x = self.col * self.tile_size + self.tile_size // 2
            self.target_y = self.row * self.tile_size + self.tile_size // 2

    def update(self):
        """현재 위치를 목표 위치로 이동"""
        if self.x < self.target_x:
            self.x = min(self.x + self.speed, self.target_x)
        elif self.x > self.target_x:
            self.x = max(self.x - self.speed, self.target_x)

        if self.y < self.target_y:
            self.y = min(self.y + self.speed, self.target_y)
        elif self.y > self.target_y:
            self.y = max(self.y - self.speed, self.target_y)

    def is_moving(self):
        return self.x != self.target_x or self.y != self.target_y
    
    def apply_item_effect(self, item_type):
        """아이템 효과 적용"""
        if item_type == "speedup":
            self.speed = min(self.speed + 2, 20)  # 속도 증가 (최대 20 제한)
        elif item_type == "boomup":
            self.max_bombs = min(self.max_bombs + 1, 5)  # 설치 가능한 폭탄 개수 증가 (최대 5 제한)
        elif item_type == "powerup":
            self.explosion_power = min(self.explosion_power + 1, 5)  # 폭발 범위 증가 (최대 5 제한)


    def draw(self, draw, image):
        """플레이어 그리기"""
        image.paste(
            self.image,
            (int(self.x - self.tile_size // 2), int(self.y - self.tile_size // 2)),
            self.image,
        )
        