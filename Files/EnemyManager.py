from Enemy import Enemy
from Boss import Boss
import random

class EnemyManager:
    @staticmethod
    def spawn_enemies(map_data, num_enemies, tile_size, sprite_folder, round_number):
        enemy_image = EnemyManager.get_enemy_image(round_number)

        # 라운드마다 다른 적의 체력 설정
        if round_number == 1:
            health = 1
        elif round_number == 2:
            health = 2 
        else:
            health = 3

        enemies = []
        for _ in range(num_enemies):
            row, col = random.choice([(r, c) for r in range(len(map_data)) for c in range(len(map_data[0])) if map_data[r][c] == "road"])
            enemy = Enemy(row, col, tile_size, sprite_folder, enemy_image, health)
            enemies.append(enemy)

        boss = None
        if round_number >= 3:
            boss_row, boss_col = random.choice([(r, c) for r in range(len(map_data)) 
                                                for c in range(len(map_data[0])) if map_data[r][c] == "road"])
            boss = Boss(boss_row, boss_col, tile_size, sprite_folder)
        return enemies, boss
    
    @staticmethod
    def move_enemies(map_data, enemies):
        """적의 목표 위치를 road, grass 타일 위에서 랜덤하게 설정"""
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 상, 하, 좌, 우
        for enemy in enemies:
            if not enemy.is_moving():
                row, col = int(enemy.y // enemy.tile_size), int(enemy.x // enemy.tile_size)
                possible_moves = [
                    (row + dr, col + dc)
                    for dr, dc in directions
                    if 0 <= row + dr < len(map_data)
                    and 0 <= col + dc < len(map_data[0])
                    and map_data[row + dr][col + dc] in ["road", "grass"]
                ]
                if possible_moves:
                    new_row, new_col = random.choice(possible_moves)
                    enemy.set_target(new_row, new_col)

    @staticmethod
    def get_enemy_image(round_number):
        """라운드에 따라 적이미지 변경"""
        if round_number == 1:
            return "enemy1.png"
        elif round_number == 2:
            return "enemy2.png"
        elif round_number >= 3:
            return "enemy3.png"

    @staticmethod
    def draw_enemies(image, enemies):
        for enemy in enemies:
            enemy.draw(image)