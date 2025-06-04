import pygame
from globals import screen 

def is_clicked_on(rect: pygame.Rect, event_list: list[pygame.event.Event]) -> bool:
    mouse_pos = pygame.mouse.get_pos()
    if rect.collidepoint(mouse_pos):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                return True
    return False

def is_clicked_elsewhere(rect: pygame.Rect, event_list: list[pygame.event.Event]) -> bool:
    mouse_pos = pygame.mouse.get_pos()
    if not rect.collidepoint(mouse_pos):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                return True
    return False

def pressed_left_click(event_list: list[pygame.event.Event]) -> bool:
    for event in event_list:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return True

def pressed_right_click(event_list: list[pygame.event.Event]) -> bool:
    for event in event_list:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            return True

def display_text(text: str, color: tuple[int], font: pygame.font.Font, x: int, y: int) -> None:
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def display_image(image: pygame.Surface, x: int, y: int, scaling: int) -> None:
    image.set_colorkey((0, 0, 0))
    image = pygame.transform.scale(image, (scaling, scaling))
    image_rect = image.get_rect(center=(x, y))
    screen.blit(image, image_rect)

def display_health_bar(self, current_health: int, base_health: int, health_bar_color: tuple[int], override_size: int = None, override_gap: int = None) -> None:
    if override_size is None:
        healthBar = pygame.Rect(0, 0, self.size, 2)
        healthBar.center = ((self.pos[0], self.pos[1]+15))
        healthBar.width = (current_health/base_health)*self.size
        pygame.draw.rect(screen, health_bar_color, healthBar)
        outline = pygame.Rect(0, 0, self.size, 4)
        outline.center = ((self.pos[0], self.pos[1]+15))
        pygame.draw.rect(screen, health_bar_color, outline, width=1)
    else:
        healthBar = pygame.Rect(0, 0, override_size, 2)
        healthBar.center = ((self.pos[0], self.pos[1]+override_gap))
        healthBar.width = (current_health/base_health)*override_size
        pygame.draw.rect(screen, health_bar_color, healthBar)
        outline = pygame.Rect(0, 0, override_size, 4)
        outline.center = ((self.pos[0], self.pos[1]+override_gap))
        pygame.draw.rect(screen, health_bar_color, outline, width=1)

def find_distance(pos1: list[int], pos2: list[int]) -> float:
    dx = pos1[0] - pos2[0]
    dy = pos1[1] - pos2[1]

    distance = (dx**2+dy**2)**0.5

    return distance