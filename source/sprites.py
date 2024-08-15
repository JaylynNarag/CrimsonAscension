from settings import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf = pygame.Surface((TILE_SIZE,TILE_SIZE)), groups = None):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)
        self.old_rect = self.rect.copy()

class AnimatedSprite(Sprite):
    def __init__(self, pos, frames, groups, animation_speed=ANIMATION_SPEED):
        if isinstance(frames, pygame.Surface):
            frames = [frames]
        
        self.frames = frames
        self.frame_index = 0
        self.animation_speed = animation_speed
        super().__init__(pos, self.frames[self.frame_index], groups)

    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self, dt):
        self.animate(dt)

class Chest(Sprite):
    def __init__(self, pos, frames, groups, player, restore_amount=20):
        super().__init__(pos, frames[0], groups)
        self.frames = frames
        self.player = player
        self.restore_amount = restore_amount
        self.is_open = False

    def interact(self):
        if not self.is_open and self.rect.colliderect(self.player.rect):
            self.is_open = True
            self.image = self.frames[1]  # Assuming the second frame is the open chest
            self.player.current_health = min(self.player.max_health, self.player.current_health + self.restore_amount)

        
