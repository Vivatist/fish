import random
from base_classes import UnderwaterSubject
import settings
from abc import ABC, abstractmethod
import base_classes


class MovieBubble(ABC):
    @abstractmethod
    def do_movie(self, obj, speed):
        pass


class StandartMovieBubble(MovieBubble):
    def __init__(self) -> None:
        self.__delta_x = 0
        self.__delta_y = 0
        self.dispersion = random.uniform(-0.07, 0.07)
        super().__init__()

    def do_movie(self, obj, speed):
        self.__delta_x += self.dispersion
        if abs(self.__delta_x) >= 1:
            obj.rect.x += int(self.__delta_x)
            self.__delta_x %= 1

        self.__delta_y += speed / settings.FPS
        if self.__delta_y >= 1:
            obj.rect.y -= int(self.__delta_y)
            self.__delta_y %= 1


class GaussMovieBubble(MovieBubble):
    def __init__(self) -> None:
        self.__delta_x = 0
        self.__delta_y = 0
        self.dispersion = (random.gauss(2, 1) - 2) / 15
        super().__init__()

    def do_movie(self, obj, speed):
        self.__delta_x += self.dispersion
        if abs(self.__delta_x) >= 1:
            obj.rect.x += int(self.__delta_x)
            self.__delta_x %= 1

        self.__delta_y += speed / settings.FPS
        if self.__delta_y >= 1:
            obj.rect.y -= int(self.__delta_y)
            self.__delta_y %= 1


class Bubble (UnderwaterSubject):
    __bubble_sprites = ['bubble1.png', 'bubble2.png',
                        'bubble3.png', 'bubble4.png']

    def __init__(self, x, y, scene, movie: MovieBubble):
        super().__init__(x, y, scene.all_sprites, scene.screen)
        self.__speed = random.randint(30, 100)  # пикселей в секунду
        self.__movie = movie

    def update(self):
        self.__movie.do_movie(self, self.__speed)
        self.lives -= 0.5
        if self.rect.top < 0:
            self.kill()
        return super().update()

    def set_sprite(self):
        self.apply_sprite(random.choice(self.__bubble_sprites))


class BubbleGenerator(base_classes.Generator):
    def __init__(self, x, y, bubble_per_second, scene) -> None:
        self.x = x
        self.y = y
        self.scene = scene
        self.clock = self.scene.clock
        self.period_msec = 1000 // bubble_per_second
        self.current_period = 0

    def update(self):
        time = self.clock.get_time()
        self.current_period += time
        if self.current_period >= self.period_msec:
            Bubble(self.x, self.y, self.scene, GaussMovieBubble())
            self.current_period = self.period_msec - self.current_period


class TestAnimationClass (UnderwaterSubject):
    def __init__(self, x, y, sprites_group, screen):
        super().__init__(x, y, sprites_group, screen)
