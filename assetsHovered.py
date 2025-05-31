import pygame

def color_match(c1, c2, tolerance=100):
    return all(abs(c1[i] - c2[i]) <= tolerance for i in range(3))

# Load your original image
image = pygame.image.load("assets/ArcherTower.png").convert()

# Background color to replace
background = (0, 0, 0)
old_color = (168, 96, 216)  # for example
new_color = (210, 150, 255)  #lighter purple

# Create a new surface with the same size
hover_ArcherTower = pygame.Surface(image.get_size())

# Optional: copy transparency if you're using it
hover_ArcherTower = hover_ArcherTower.convert()
hover_ArcherTower.set_colorkey(background)

# Pixel-by-pixel replacement
for x in range(image.get_width()):
    for y in range(image.get_height()):
        current_color = image.get_at((x, y))[:3]
        if color_match(current_color, old_color):
            hover_ArcherTower.set_at((x, y), new_color)
        else:
            hover_ArcherTower.set_at((x, y), current_color)
