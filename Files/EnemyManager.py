from Enemy import Enemy
import random

class EnemyManager:
    @staticmethod
    def spawn_enemies(map_data, num_enemies, tile_size, sprite_folder):
        """맵 데이터에서 회색 타일(road) 위에 적을 랜덤 스폰"""
        road_tiles = [
            (row_idx, col_idx)
            for row_idx, row in enumerate(map_data)
            for col_idx, tile_type in enumerate(row)
            if tile_type == "road"
        ]
        enemy_positions = random.sample(road_tiles, num_enemies)
        return [Enemy(row, col, tile_size, sprite_folder) for row, col in enemy_positions]

    @staticmethod
    def move_enemies(map_data, enemies):
        """적의 목표 위치를 회색 타일(road) 위에서 랜덤하게 설정"""
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
    def draw_enemies(image, enemies):
        """적을 화면에 작은 원으로 표시"""
        for enemy in enemies:
            enemy.draw(image)