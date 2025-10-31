from pygame import Rect


class Paddle:
    def __init__(self, screen_width, screen_height, position, width=20, height=100):
        self.screen_width = screen_width
        self.screen_height = screen_height
        if position not in ["left", "right"]:
            raise ValueError("Paddle position must be 'left' or 'right'")
        self.color = (255, 0, 0) if position == "left" else (0, 0, 255)

        x_pos = screen_width / 7 if position == "left" else screen_width * 6 / 7 - width
        y_pos = screen_height / 2 - height / 2
        self.rect = Rect(x_pos, y_pos, width, height)

    def move(self, dy):
        if self.rect.top + dy < 0:
            self.rect.y = 0
        elif self.rect.bottom + dy > self.screen_height:
            self.rect.y = self.screen_height - self.rect.height
        else:
            self.rect.move_ip(0, dy)
