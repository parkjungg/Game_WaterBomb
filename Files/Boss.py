from Enemy import Enemy
import random

class Boss(Enemy):
    def __init__(self, start_row, start_col, tile_size, sprite_folder):
        super().__init__(start_row, start_col, tile_size, sprite_folder, "boss.png", health=7)

    def move(self, map_data):
        if not self.is_moving():
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 상, 하, 좌, 우
            row, col = int(self.y // self.tile_size), int(self.x // self.tile_size)
            possible_moves = [
                (row + dr, col + dc)
                for dr, dc in directions
                if 0 <= row + dr < len(map_data)
                and 0 <= col + dc < len(map_data[0])
                and map_data[row + dr][col + dc] in ["road", "grass"]
            ]
            if possible_moves:
                new_row, new_col = random.choice(possible_moves)
                self.set_target(new_row, new_col)