from PIL import Image, ImageDraw
import os
from Player import Player
from JoyStick import Joystick 
from EnemyManager import EnemyManager
from Background import Background
from Bomb import Bomb
from Item import Item
from random import random, choice
import time

background = Background(width=240, height=240)

def main():
    sprite_folder = os.path.join(os.path.dirname(__file__), "Sprite")
    # Joystick 클래스 초기화
    joystick = Joystick()

    # Joystick 화면 크기 가져오기
    width, height = joystick.width, joystick.height
    tile_size = 30  # 타일 크기

    # 고정된 8x8 맵 데이터 정의
    map_data = [
        ["grass", "road", "box", "box", "grass", "road", "box", "box"],
        ["road", "road", "grass", "box", "box", "grass", "road", "box"],
        ["box", "road", "grass", "road", "box", "road", "box", "box"],
        ["box", "road", "box", "grass", "grass", "box", "box", "grass"],
        ["grass", "road", "road", "box", "road", "grass", "road", "box"],
        ["road", "box", "box", "grass", "box", "road", "box", "grass"],
        ["grass", "road", "box", "box", "grass", "road", "box", "box"],
        ["road", "road", "grass", "road", "box", "grass", "road", "box"]
    ]
    # 폭탄 관리 리스트
    bombs = []
    # 아이템 관리 리스트
    items = []
    key_dropped = False # 열쇠 아이템의 드랍 여부 판단

    # 플레이어 랜덤 위치 생성
    player = Player(map_data, tile_size, sprite_folder)

    # 적 스폰
    num_enemies = 5
    enemies = EnemyManager.spawn_enemies(map_data, num_enemies, tile_size, sprite_folder)

    # 게임 시작 화면 처리
    frame = 0
    while True:
        my_image = Image.new("RGB", (background.width, background.height))
        my_draw = ImageDraw.Draw(my_image)
        background.draw_start_screen(my_draw, frame)
        joystick.disp.image(my_image)

        # 특정 버튼 (예: A버튼)을 눌렀는지 확인
        if joystick.is_pressed(joystick.button_A):
            print("게임 시작 버튼 클릭!")
            break  # 게임 시작 루프 종료

        frame += 1  # 프레임 증가
        time.sleep(0.1)

    my_image = Image.new("RGB", (background.width, background.height))
    my_draw = ImageDraw.Draw(my_image)
    background.draw_map(my_draw, map_data, my_image)  # 맵 그리기
    background.draw_title_screen(my_draw, "Round 1")  # 타이틀 그리기
    joystick.disp.image(my_image)

    time.sleep(2) # 2초 뒤에 게임 시작

    player_dead = False
    time_of_death = None

    # 메인 게임 루프
    while True:
        # Joystick 화면에 맞는 빈 캔버스 생성
        my_image = Image.new("RGB", (background.width, background.height))
        my_draw = ImageDraw.Draw(my_image)

        # 맵 타일 그리기
        background.draw_map(my_draw, map_data, my_image)

        # 폭탄 그리기
        for bomb in bombs[:]:
            bomb.timer -= 0.05  # 타이머 감소
            if bomb.timer <= 0 and not bomb.exploded:
                # 폭발 처리
                bomb.exploded = True
                bomb.timer = bomb.effect_duration  # 이펙트 지속 시간으로 설정

                # 폭발 범위 타일 업데이트
                explosion_range = bomb.get_explosion_range(map_data, player.explosion_power)

                # 폭발 범위에 플레이어가 있으면 게임 종료
                if (player.row, player.col) in explosion_range:
                    player_dead = True
                    time_of_death = time.time()

                # 폭발 범위에 있는 적 제거
                enemies = [
                    enemy for enemy in enemies
                    if (int(enemy.y // tile_size), int(enemy.x // tile_size)) not in explosion_range
                ]
                # 폭발 범위 내 박스를 road로 변경
                for r, c in explosion_range:
                    if map_data[r][c] == "box":
                        map_data[r][c] = "road"
                        if not key_dropped and random() < 0.1:  # 10% 확률로 열쇠 드랍
                            items.append(Item(r, c, "key", tile_size, sprite_folder))
                            key_dropped = True
                        elif random() < 0.3:  # 30% 확률로 다른 아이템 드랍
                            item_type = choice(["speedup", "boomup", "powerup"])
                            items.append(Item(r, c, item_type, tile_size, sprite_folder))
            elif bomb.exploded and bomb.timer <= 0:
                bombs.remove(bomb)  # 이펙트 종료 후 폭탄 제거

            bomb.draw(my_image, map_data, player.explosion_power)

        # 아이템 그리기
        for item in items:
            item.draw(my_image)  

        # 적 이동 및 그리기
        EnemyManager.move_enemies(map_data, enemies)
        EnemyManager.draw_enemies(my_image, enemies)

        # 플레이어 이동
        if not player_dead and not player.is_moving():
            if joystick.is_pressed(joystick.button_U):
                player.set_target("up")
            elif joystick.is_pressed(joystick.button_D):
                player.set_target("down")
            elif joystick.is_pressed(joystick.button_L):
                player.set_target("left")
            elif joystick.is_pressed(joystick.button_R):
                player.set_target("right")

        # 플레이어 그리기        
        if not player_dead:
            player.update()
            player.draw(my_draw, my_image)
    
        # Joystick 화면에 출력
        joystick.disp.image(my_image)

        # 게임 종료
        if player_dead and time.time() - time_of_death >= 2:
            break

        # 적 업데이트
        for enemy in enemies:
            enemy.update()
            enemy.draw(my_image)

        # 폭탄 설치
        if not player_dead and joystick.is_pressed(joystick.button_A):
            if len(bombs) < player.max_bombs:
                bombs.append(Bomb(player.row, player.col, tile_size, sprite_folder, map_data))

        # 적과 플레이어 충돌 확인
        if not player_dead:
            for enemy in enemies:
                enemy_row, enemy_col = int(enemy.y // tile_size), int(enemy.x // tile_size)
                if(player.row, player.col) == (enemy_row, enemy_col):
                    player_dead = True
                    time_of_death = time.time()
                    break  

        # 아이템 획득 확인 및 처리
        for item in items[:]: 
            if (player.row, player.col) == (item.row, item.col):
                player.apply_item_effect(item.item_type)
                items.remove(item)          

        # 화면 업데이트 속도 조절
        time.sleep(0.05)

if __name__ == '__main__':
    main()