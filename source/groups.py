from settings import *

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = vector()

    def draw(self, target_pos): # set level + camera following character
        self.offset.x = -(target_pos[0] - WINDOW_WIDTH / 2) # divides by 2 = character centre of window always + invert to follow character
        self.offset.y = -(target_pos[1] - WINDOW_HEIGHT / 2) # divides by 2 = character centre of window always + invert to follow character

        for sprite in self:
            offset_pos = sprite.rect.topleft + self.offset
            self.display_surface.blit(sprite.image, offset_pos)
