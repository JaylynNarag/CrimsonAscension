from settings import *
import pygame
from random import choice
from timer import Timer

class Zombie(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, floor_sprites, platform_sprites):
        super().__init__(groups)
        self.frames = frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_frect(topleft=pos)
        
        self.direction = choice((-1, 1))  # Random initial direction        
        self.floor_sprites = floor_sprites
        self.platform_sprites = platform_sprites
        self.collision_rects = [sprite.rect for sprite in (floor_sprites.sprites() + platform_sprites.sprites())]
        self.speed = 50

    def update(self, dt):
        self.frame_index += ANIMATION_SPEED * dt
        self.image = self.frames[int(self.frame_index % len(self.frames))]
        if self.direction > 0:
            self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.image
            
        self.rect.x += self.direction * self.speed * dt
        floor_rect_right = pygame.FRect(self.rect.bottomright, (1,1))
        floor_rect_left = pygame.FRect(self.rect.bottomleft, (-1,1))

        if floor_rect_right.collidelist(self.collision_rects) < 0 and self.direction > 0 or\
           floor_rect_left.collidelist(self.collision_rects) < 0 and self.direction < 0:
            self.direction *= -1

class SkeletonArcher(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, floor_sprites, platform_sprites, player, arrow):
        super().__init__(groups)
        self.frames = frames
        self.frame_index = 0
        self.state = 'idle'
        self.image = self.frames[self.state][self.frame_index]
        self.rect = self.image.get_frect(topleft=pos)

        self.floor_sprites = floor_sprites
        self.platform_sprites = platform_sprites
        self.collision_rects = [sprite.rect for sprite in (floor_sprites.sprites() + platform_sprites.sprites())]
        self.shoot_timer = Timer(2000, self.shoot_arrow, repeat=True)  # Set to shoot every 2 seconds
        self.arrow = arrow
        self.player = player

        # Set the arrow direction to always be left (-1)
        self.arrow_direction = -1

        self.align_with_platform()
        self.shoot_timer.activate()

    def align_with_platform(self):
        floor_rect = pygame.FRect(self.rect.midbottom, (1, 1))
        collision_index = floor_rect.collidelist(self.collision_rects)
        if (collision_index >= 0):
            self.rect.bottom = self.collision_rects[collision_index].top

    def shoot_arrow(self):
        self.state = 'attack'
        self.frame_index = 0
        self.arrow(self.rect.center, self.arrow_direction)

    def update(self, dt):
        self.shoot_timer.update()

        self.frame_index += ANIMATION_SPEED * dt
        if self.frame_index < len(self.frames[self.state]):
            self.image = self.frames[self.state][int(self.frame_index)]
        else:
            self.frame_index = 0
            self.state = 'idle'


class Arrow(pygame.sprite.Sprite):
    def __init__(self, pos, groups, surf, direction, speed, floor_sprites, platform_sprites, player):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center=pos + vector(50 * direction, 0))
        self.direction = direction
        self.speed = speed
        self.collision_sprites = floor_sprites.sprites() + platform_sprites.sprites()
        self.player = player  # Reference to the player character

    def update(self, dt):
        self.rect.x += self.direction * self.speed * dt

        # Check collision with walls, floors, platforms - so doesn't keep going through map
        for sprite in self.collision_sprites:
            if self.rect.colliderect(sprite.rect):
                self.kill()
                break

        # collision with player - takes damage
        if self.rect.colliderect(self.player.hitbox_rect):
            self.kill()


