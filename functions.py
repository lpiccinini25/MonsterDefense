import pygame
from globals import screen

def is_clicked_on(rect, event_list) -> bool:
    mouse_pos = pygame.mouse.get_pos()
    if rect.collidepoint(mouse_pos):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                return True
    return False

def is_clicked_elsewhere(rect, event_list) -> bool:
    mouse_pos = pygame.mouse.get_pos()
    if not rect.collidepoint(mouse_pos):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                return True
    return False

def display_text(text, color, font, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def display_image(image, x, y, scaling):
    image.set_colorkey((0, 0, 0))
    image = pygame.transform.scale(image, (scaling, scaling))
    image_rect = image.get_rect(center=(x, y))
    screen.blit(image, image_rect)
