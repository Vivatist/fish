# Pygame шаблон - скелет для нового проекта Pygame
import pygame
import settings
from base_classes import TextScreenInfo, Group
from game_classes import Bubble, BubbleGenerator, GaussMovieBubble
from os import path


class Scene():
    def __init__(self, display, clock, ) -> None:
        self.screen = display.set_mode((settings.WIDTH, settings.HEIGHT))

        self.text = TextScreenInfo(self.screen, 5, 5)
        self.clock = clock
        # Загрузка всей игровой графики
        self.background = pygame.image.load(path.join(settings.img_dir,
                                            "Empty-Aquarium-Background.jpg")).convert()  # noqa: E501 (игнор ошибки Flake8, можно убрать)
        self.background_rect = self.background.get_rect()
        self.all_sprites = pygame.sprite.Group()

        # Расставляем генераторы пузырьков
        self.bubble_generators_group = Group()
        self.bubble_generators_group.add(BubbleGenerator(542, 549, 2, self))
        self.bubble_generators_group.add(BubbleGenerator(988, 543, 5, self))
        self.bubble_generators_group.add(BubbleGenerator(96, 539, 10, self))
        self.bubble_generators_group.add(BubbleGenerator(464, 349, 6, self))
        self.bubble_generators_group.add(BubbleGenerator(464, 349, 50, self))
        self.bubble_generators_group.add(BubbleGenerator(464, 349, 50, self))
        self.bubble_generators_group.add(BubbleGenerator(464, 349, 50, self))


        self.counter = 0

    def show_information(self):
        self.text.print(f'all_sprites: {len(self.all_sprites)}')
        self.text.print('FPS: %d' % self.clock.get_fps())
        self.text.print(f'x: {x}, y: {y}')
        self.text.print(f'get_time: {self.clock.get_time()} мсек')
        self.text.print(f'счетчик кадров: {self.counter}')
        self.text.reset()

    def update(self):
        self.counter = (self.counter + 1) % settings.FPS
        self.clock.tick(settings.FPS)  # держим цикл на правильной скорости
        self.screen.blit(self.background, self.background_rect)

        # Обновление
        self.all_sprites.update()
        self.bubble_generators_group.update()

        self.all_sprites.draw(self.screen)

        # после отрисовки всего, переворачиваем экран
        self.show_information()
        display.flip()


# создаем игру и окно
pygame.init()
pygame.mixer.init()  # для звука
display = pygame.display
display.set_caption("Рыбки любят где поглубже")
clock = pygame.time.Clock()
scene = Scene(display, clock)
x, y = None, None
# Цикл игры
running = True
while running:
    # обходим все события окна
    for event in pygame.event.get():
        # проверить закрытие окна
        if event.type == pygame.QUIT:
            running = False
        # при нажатии мышки
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            unknown_obj = Bubble(x, y, scene, GaussMovieBubble())
        elif event.type == pygame.MOUSEMOTION:
            x, y = event.pos
            unknown_obj = Bubble(x, y, scene, GaussMovieBubble())
            unknown_obj = Bubble(x, y, scene, GaussMovieBubble())
            unknown_obj = Bubble(x, y, scene, GaussMovieBubble())

    scene.update()


pygame.quit()  # выходим из приложения
