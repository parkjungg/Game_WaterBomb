import os
from PIL import Image, ImageFont

class Background:
    def __init__(self, width, height, tile_size=30):
        self.width = width
        self.height = height
        self.tile_size = tile_size
        
        sprite_folder = os.path.join(os.path.dirname(__file__), "Sprite")
        
        # 타일 색상 정의
        self.tile_images = {
            "grass" : Image.open(os.path.join(sprite_folder, "tile0.png")).resize((tile_size, tile_size)),
            "road" : Image.open(os.path.join(sprite_folder, "tile1.png")).resize((tile_size, tile_size)),
            "box" : Image.open(os.path.join(sprite_folder, "block0.png")).resize((tile_size, tile_size))
        }
        
        # 폰트 설정
        self.font_path = "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"
        if not os.path.exists(self.font_path):
            raise FileNotFoundError(f"폰트 파일이 {self.font_path}에 없습니다. 적절한 경로를 설정하세요.")
        self.font = ImageFont.truetype(self.font_path, 24)  # 기본 폰트 크기 24

    def draw_map(self, draw, map_data, canvas):
        # 맵 그리기(png 파일 이용)
        for row_idx, row in enumerate(map_data):
            for col_idx, tile_type in enumerate(row):
                x = col_idx * self.tile_size
                y = row_idx * self.tile_size

                tile_image = self.tile_images.get(tile_type)
                if tile_image:
                    canvas.paste(tile_image, (x, y)) # 이미지 그리기               

    def draw_start_screen(self, draw, frame):
        """게임 시작 화면 그리기"""
        draw.rectangle([0, 0, self.width, self.height], fill=(0, 0, 0))  # 검정 배경

        # 텍스트와 버튼 그리기
        text = "게임 시작"
        text_width, text_height = draw.textsize(text, font=self.font)
        draw.text(
            ((self.width - text_width) // 2, (self.height - text_height) // 2),
            text,
            fill=(255, 255, 255),
            font=self.font
        )

        # 버튼 테두리 반짝이는 효과
        colors = [(255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 255, 0), 
                  (0, 255, 255), (0, 0, 255), (255, 0, 255)]
        border_color = colors[frame % len(colors)]  # 색상을 순환

        draw.rectangle(
            [self.width // 2 - 60, self.height // 2 - 40, 
             self.width // 2 + 60, self.height // 2 + 40],
            outline=border_color,
            width=4
        )

    def is_button_clicked(self, joystick):
        """버튼 클릭 확인"""
        x, y = joystick.get_touch_coordinates()  # 터치 좌표 가져오기
        if (self.width // 2 - 60 <= x <= self.width // 2 + 60 and 
                self.height // 2 - 40 <= y <= self.height // 2 + 40):
            return True
        return False
    def draw_title_screen(self, draw, title):
        """화면 중앙에 타이틀 텍스트 그리기"""
        text_width, text_height = draw.textsize(title, font=self.font)
        x = (self.width - text_width) // 2
        y = (self.height - text_height) // 2
        draw.text((x, y), title, fill=(255, 255, 255), font=self.font)