__author__ = 'skydreamer'
import os
import pygame
import const


def load_image(name):
    fullname = os.path.join('content', name)
    try:
        image = pygame.image.load(fullname)
        image = pygame.transform.scale(image, (const.WINDOW_WIDTH, const.WINDOW_HEIGHT))
    except pygame.error:
        print 'Cannot load image:', name
        raise SystemExit
    image = image.convert()
    return image, image.get_rect()