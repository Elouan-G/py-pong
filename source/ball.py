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

    def move(self, dist):
        dist = self.__bounce_and_reset(dist)
        self.x_pos += self.direction[0] * dist
        self.y_pos += self.direction[1] * dist

    def __bounce_and_reset(self, dist) -> float:
        """Updates direction vector and returns the distance left to travel after any bounce or reset required."""
        next_x = self.x_pos + self.direction[0] * dist
        next_y = self.y_pos + self.direction[1] * dist

        # Bounce off top
        if next_y - self.radius < 0:
            self.direction[1] *= -1
            dist += next_y - self.radius
            return dist if dist > 0 else 0

        # Bounce off bottom
        if next_y + self.radius > self.screen_height:
            self.direction[1] *= -1
            dist -= next_y + self.radius - self.screen_height
            return dist if dist > 0 else 0

        # Reset on left or right border
        if next_x - self.radius < 0 or next_x + self.radius > self.screen_width:
            self.x_pos = self.screen_width / 2
            self.y_pos = self.screen_height / 2
            return 0

        # Bounce off left paddle
        if (
            next_x - self.radius < self.__left_paddle.rect.right
            and next_x - self.radius > self.__left_paddle.rect.left
            and next_y + self.radius > self.__left_paddle.rect.top
            and next_y - self.radius < self.__left_paddle.rect.bottom
            and self.direction[0] == -1
        ):
            self.direction[0] *= -1
            dist += next_x - self.radius - self.__left_paddle.rect.right
            return dist if dist > 0 else 0

        # Bounce off right paddle
        if (
            next_x + self.radius > self.__right_paddle.rect.left
            and next_x + self.radius < self.__right_paddle.rect.right
            and next_y + self.radius > self.__right_paddle.rect.top
            and next_y - self.radius < self.__right_paddle.rect.bottom
            and self.direction[0] == 1
        ):
            self.direction[0] *= -1
            dist -= next_x + self.radius - self.__right_paddle.rect.left
            return dist if dist > 0 else 0

        # No bounce or reset needed
        return dist
