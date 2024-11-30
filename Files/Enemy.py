from PIL import Image
import os
class Enemy:
    """적 클래스 정의"""
    def __init__(self, start_row, start_col, tile_size, sprite_folder, enemy_image, health):
        self.x = start_col * tile_size + tile_size // 2  # 적의 초기 X 위치 (픽셀 단위)
        self.y = start_row * tile_size + tile_size // 2  # 적의 초기 Y 위치 (픽셀 단위)
        self.target_x = self.x  # 목표 X 위치
        self.target_y = self.y  # 목표 Y 위치
        self.tile_size = tile_size
        self.speed = 2  # 이동 속도
        self.health = health
        self.image = Image.open(os.path.join(sprite_folder, enemy_image)).resize((tile_size, tile_size))

    def update(self):
        """적의 현재 위치를 목표 위치로 점진적으로 이동"""
        if self.x < self.target_x:
            self.x = min(self.x + self.speed, self.target_x)
        elif self.x > self.target_x:
            self.x = max(self.x - self.speed, self.target_x)

        if self.y < self.target_y:
            self.y = min(self.y + self.speed, self.target_y)
        elif self.y > self.target_y:
            self.y = max(self.y - self.speed, self.target_y)

    def set_target(self, new_row, new_col):
        """적의 목표 위치를 설정 (타일 좌표를 픽셀 좌표로 변환)"""
        self.target_x = new_col * self.tile_size + self.tile_size // 2
        self.target_y = new_row * self.tile_size + self.tile_size // 2

    def is_moving(self):
        """적이 아직 목표 위치로 이동 중인지 확인"""
        return self.x != self.target_x or self.y != self.target_y
    
    def take_damage(self, damage = 1):
        self.health -= damage
    
    def is_dead(self):
        return self.health <= 0
    
    def draw(self, image):
        image.paste(
            self.image,
            (int(self.x - self.tile_size // 2), int(self.y - self.tile_size // 2)),
            self.image,
        )