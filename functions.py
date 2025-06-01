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

def button(x, y, w, h, text, color, hover_color, text_color, text_font, action=None):
    rect = pygame.Rect(x, y, 100, 50)
    clicked = False

    rect.center = (x, y)
    pygame.draw.rect(screen, color, rect)
    display_text(text, text_color, text_font, x, y)

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+int(w/2) > mouse[0] > x-int(w/2) and y+int(h/2) > mouse[1] > y-int(h/2):
        if click[0] == 1 and action != None:
            action()