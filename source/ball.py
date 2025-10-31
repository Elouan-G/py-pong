class Ball:
    def __init__(
        self, screen_width, screen_height, left_paddle, right_paddle, radius=10
    ):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.__left_paddle = left_paddle
        self.__right_paddle = right_paddle
        self.radius = radius
        self.color = (255, 255, 255)
        self.x_pos = screen_width / 2
        self.y_pos = screen_height / 2
        self.direction = [1, 1]

    def move(self, d):
        next_x = self.x_pos + self.direction[0] * d
        next_y = self.y_pos + self.direction[1] * d

        # Bounces off top and bottom
        if next_y - self.radius < 0 or next_y + self.radius > self.screen_height:
            self.direction[1] *= -1

        # Bounces off left paddle
        elif (
            next_x - self.radius < self.__left_paddle.rect.right
            and next_y + self.radius > self.__left_paddle.rect.top
            and next_y - self.radius < self.__left_paddle.rect.bottom
        ):
            self.direction[0] *= -1

        # Bounces off right paddle
        elif (
            next_x + self.radius > self.__right_paddle.rect.left
            and next_y + self.radius > self.__right_paddle.rect.top
            and next_y - self.radius < self.__right_paddle.rect.bottom
        ):
            self.direction[0] *= -1

        # Updates position with direction changes
        self.x_pos += self.direction[0] * d
        self.y_pos += self.direction[1] * d

        # Resets we if out of bounds (left or right)
        if self.x_pos - self.radius < 0 or self.x_pos + self.radius > self.screen_width:
            self.x_pos = self.screen_width / 2
            self.y_pos = self.screen_height / 2
            self.direction = [1, 1]
