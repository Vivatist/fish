import pygame
from enum import Enum
from os import path
import settings
from abc import ABC, abstractmethod


class Direction(Enum):
    stop = 0
    left = -1
    right = 1


'''Описания классов вывода текста'''


class Text():
    def __init__(self, screen, font_name,
                 font_size, font_color, alpha=255) -> None:
        self.font = pygame.font.SysFont(font_name, font_size)
        self.alpha = alpha
        self.color = font_color
        self.screen = screen
        self.current_string = 0

    def print(self, text, x, y):
        text_surf = self.font.render(text, True, self.color)
        text_surf.set_alpha(self.alpha)
        self.screen.blit(text_surf, text_surf.get_rect(topleft=(x, y)))


class TextScreenInfo(Text):
    def __init__(self, screen, x, y) -> None:
        self.font_name = 'Arial'
        self.font_size = 12
        self.font_color = (255, 255, 255)
        self.x = x
        self.y = y
        self.alpha = 127
        self.color = settings.WHITE
        self.screen = screen
        self.current_string = 0
        super().__init__(screen, self.font_name, self.font_size,
                         self.font_color, self.alpha)

    def print(self, text):
        y_string = (self.font_size + 2) * self.current_string
        super().print(text, self.x, self.y + y_string)
        self.current_string += 1

    def reset(self):
        self.current_string = 0


'''Описание базовых классов подводношо мира'''


class UnderwaterSubject(pygame.sprite.Sprite):

    def __init__(self, x, y, sprites_group, screen):
        pygame.sprite.Sprite.__init__(self)
        self.view_info = False
        self.lives = 100  # Жизни в процентах 0-100
        self.x = x
        self.y = y
        self.set_sprite()
        self.text = Text(screen, 'Arial', 10, settings.WHITE)
        sprites_group.add(self)

    def show_info(self, view_info: bool):
        if not view_info:
            return
        x, y = self.rect.topright[0], self.rect.topright[1]
        height_string = 10
        self.text.print(f'жизни: {self.lives}', x, y)
        self.text.print(f'x: {self.rect.x}, y: {self.rect.y}',
                        x, y + height_string)

    def update(self):
        if self.lives <= 0:
            self.kill()
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_1]:
            self.view_info = True
        elif keystate[pygame.K_2]:
            self.view_info = False
        self.show_info(self.view_info)

    def apply_sprite(self, file_name: str):
        self.image = pygame.image.load(path.join(settings.img_dir,
                                       file_name)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def set_sprite(self):
        self.apply_sprite('underwater_subject.png')


class Group():
    def __init__(self) -> None:
        self.list = list()

    def update(self):
        for obj in self.list:
            obj.update()

    def add(self, obj):
        self.list.append(obj)

    def remove(self, obj):
        try:
            self.list.remove(obj)
        except ValueError:
            print(ValueError)
            raise Exception("ERROR: Attempt to remove a missing element from a group")  # noqa: E501


class Generator(ABC):
    @abstractmethod
    def update():
        pass
