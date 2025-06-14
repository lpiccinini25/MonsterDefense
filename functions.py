import pygame
import colors
from globals import screen, GameInfo
from typing import Optional, Union

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
    return False

def pressed_right_click(event_list: list[pygame.event.Event]) -> bool:
    for event in event_list:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            return True
    return False

def display_text(text: str, color: tuple[int, int, int], font: pygame.font.Font, x: int, y: int) -> None:
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def display_rect(x: int, y: int, w: int, h: int, color: tuple[int, int, int]) -> None:
    rect = pygame.Rect(x, y, w, h)
    rect.center = (x, y)
    pygame.draw.rect(screen, color, rect)

def scale_image(image: pygame.Surface, target_width: int) -> pygame.Surface:
    original_width, original_height = image.get_size()
    aspect_ratio = original_height / original_width
    new_height = int(target_width * aspect_ratio)
    return pygame.transform.scale(image, (target_width, new_height))

def load_image_and_rect(image_string: str, width_size: int, pos: tuple[int, int]) -> tuple[pygame.Surface, pygame.Rect]:
    image: pygame.Surface = pygame.image.load("assets/"+image_string+".png").convert()
    image.set_colorkey((0, 0, 0))
    image = scale_image(image, width_size)
    image_rect = image.get_rect(center=pos)
    return image, image_rect

def load_image(image_string: str, width_size: int) -> pygame.Surface:
    image: pygame.Surface = pygame.image.load("assets/"+image_string+".png").convert()
    image.set_colorkey((0, 0, 0))
    image = scale_image(image, width_size)
    return image

def display_image_static(image: pygame.Surface, image_rect: pygame.Rect) -> None:
    screen.blit(image, image_rect)

def display_image_new_rect(image: pygame.Surface, x: int, y: int) -> None:
    image_rect = image.get_rect(center=(x, y))
    screen.blit(image, image_rect)

def display_health_bar(self, current_health: int, base_health: int, health_bar_color: tuple[int, int, int], override_size: Optional[int] = None, override_gap: Optional[int] = None) -> None:
    OUTLINE_COLOR = (100, 0, 0)
    if override_size is None:
        healthBar = pygame.Rect(0, 0, self.image_width, 2)
        healthBar.center = ((self.pos[0], self.pos[1]+15))
        healthBar.width = (current_health/base_health)*self.image_width
        pygame.draw.rect(screen, health_bar_color, healthBar)
        outline = pygame.Rect(0, 0, self.image_width, 4)
        outline.center = ((self.pos[0], self.pos[1]+15))
        pygame.draw.rect(screen, OUTLINE_COLOR, outline, width=1)
    else:
        healthBar = pygame.Rect(0, 0, override_size, 2)
        healthBar.center = ((self.pos[0], self.pos[1]+override_gap))
        healthBar.width = round((current_health/base_health)*override_size)
        pygame.draw.rect(screen, health_bar_color, healthBar)
        outline = pygame.Rect(0, 0, override_size, 4)
        outline.center = ((self.pos[0], self.pos[1]+override_gap))
        pygame.draw.rect(screen, OUTLINE_COLOR, outline, width=1)

def display_respawn_bar(self, repair_time: int, base_repair_time: int, repair_bar_color: tuple[int, int, int], override_size: Optional[int] = None, override_gap: Optional[int] = None):
    if override_size is None:
        repair_bar = pygame.Rect(0, 0, self.image_width, 2)
        repair_bar.center = ((self.pos[0], self.pos[1]+15))
        repair_bar.width = ((base_repair_time-repair_time)/base_repair_time)*self.image_width
        pygame.draw.rect(screen, repair_bar_color, repair_bar)
        outline = pygame.Rect(0, 0, self.image_width, 4)
        outline.center = ((self.pos[0], self.pos[1]+15))
        pygame.draw.rect(screen, repair_bar_color, outline, width=1)
    else:
        healthBar = pygame.Rect(0, 0, override_size, 2)
        healthBar.center = ((self.pos[0], self.pos[1]+override_gap))
        healthBar.width = round(((base_repair_time-repair_time)/base_repair_time)*override_size)
        pygame.draw.rect(screen, repair_bar_color, healthBar)
        outline = pygame.Rect(0, 0, override_size, 4)
        outline.center = ((self.pos[0], self.pos[1]+override_gap))
        pygame.draw.rect(screen, repair_bar_color, outline, width=1)


def find_distance(pos1: Union[tuple[float, float], tuple[int, int]], pos2: Union[tuple[float, float], tuple[int, int]]) -> int:
    dx = pos1[0] - pos2[0]
    dy = pos1[1] - pos2[1]

    distance = round((dx**2+dy**2)**0.5)

    return distance

def repair_tower_clicked(repair_amount: int, game_info: GameInfo, event_list: list[pygame.event.Event]) -> bool:
    for tower in game_info.all_purchasables:
        if is_clicked_on(tower.image_rect, event_list):
            if tower.current_health < tower.base_health:
                tower.repair(repair_amount)
                return True
    return False

