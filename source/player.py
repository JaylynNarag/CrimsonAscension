from settings import *
from timer import Timer
import pygame
from os.path import join

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, floor_sprites, platform_sprites, frames):
        super().__init__(groups)

        # character image
        self.frames = frames
        self.frame_index = 0
        self.state = 'idleSpriteAnim'
        self.facing_right = True
        self.image = self.frames[self.state][self.frame_index]

        # rects
        self.rect = self.image.get_frect(topleft=pos)
        self.hitbox_rect = self.rect.inflate(0, 0)
        self.old_rect = self.rect.copy()

        # movement - direction, speed, gravity, and jump attributes
        self.direction = vector()
        self.speed = 125
        self.gravity = 300  # Increased gravity for a quicker fall
        self.jump_speed = -250  # Increased jump speed for a snappier jump
        self.collision_sprites = floor_sprites
        self.platform_sprites = platform_sprites
        self.on_ground = False
        self.is_jumping = False
        self.jump_key_held = False  # Track if jump key is being held
        self.attacking = False
        self.attack_frame_count = 0  # Track the current frame in attack animation

        self.enemies = None
        self.max_health = 100
        self.current_health = self.max_health
        self.alive = True
        self.damage_cooldown = Timer(1000)

        # Initialize jump_cut_off attribute
        self.jump_cut_off = 1.5  # Adjust this value for the desired jump cutoff effect

        # Variable to track if down key is pressed
        self.down_key_pressed = False

    def input(self, dt):
        keys = pygame.key.get_pressed()

        # Handle attack input
        if (keys[pygame.K_e] or keys[pygame.K_x]):
            self.attack()

        # Handle movement input
        self.handle_movement_input(keys, dt)

    def handle_movement_input(self, keys, dt):
        input_vector = vector(0, 0)

        # left + right movement
        if keys[pygame.K_RIGHT]:
            input_vector.x = 1  # Set directly to 1
            self.facing_right = True
        elif keys[pygame.K_LEFT]:
            input_vector.x = -1  # Set directly to -1
            self.facing_right = False
        else:
            input_vector.x = 0  # Stop moving if no horizontal key is pressed

        self.direction.x = input_vector.x  # Directly assign the x component to direction.x

        # Jump logic
        if keys[pygame.K_SPACE] and not self.is_jumping and self.on_ground:
            self.direction.y = self.jump_speed
            self.is_jumping = True
            self.on_ground = False
            self.jump_key_held = True
        else:
            self.jump_key_held = False  # Reset when space is released

        if not keys[pygame.K_SPACE] and self.is_jumping:
            self.direction.y += self.gravity * dt * self.jump_cut_off  # Cut jump short if space is released

        # down key pressed to fall down platform
        self.down_key_pressed = keys[pygame.K_DOWN]

    def attack(self):
        self.attacking = True
        self.frame_index = 0
        self.attack_frame_count = len(self.frames[self.state])  # Set total frames for current state

    def end_attack(self):
        self.attacking = False

    def apply_gravity(self, dt):
        self.direction.y += self.gravity * dt

    def move(self, dt):
        if self.direction.x != 0 or not self.attacking:  # Allow movement if moving or not attacking
            self.hitbox_rect.x += self.direction.x * self.speed * dt
            self.collision('horizontal')

        # Always apply gravity and vertical movement
        self.apply_gravity(dt)
        self.hitbox_rect.y += self.direction.y * dt
        self.collision('vertical')
        self.rect.center = self.hitbox_rect.center

    def collision(self, axis):
        if axis == 'horizontal':
            for sprite in self.collision_sprites:
                if sprite.rect.colliderect(self.hitbox_rect):
                    if self.direction.x > 0:  # Moving right
                        self.hitbox_rect.right = sprite.rect.left
                    if self.direction.x < 0:  # Moving left
                        self.hitbox_rect.left = sprite.rect.right

        if axis == 'vertical':
            self.on_ground = False
            for sprite in self.collision_sprites:
                if sprite.rect.colliderect(self.hitbox_rect):
                    if self.direction.y > 0:  # Falling down
                        self.hitbox_rect.bottom = sprite.rect.top
                        self.direction.y = 0
                        self.on_ground = True
                        self.is_jumping = False  # Reset jumping state
                    if self.direction.y < 0:  # Moving up
                        self.hitbox_rect.top = sprite.rect.bottom
                        self.direction.y = 0

            for sprite in self.platform_sprites:
                if sprite.rect.colliderect(self.hitbox_rect) and self.direction.y > 0:  # Falling down
                    if self.old_rect.bottom <= sprite.rect.top:
                        if not self.down_key_pressed:
                            self.hitbox_rect.bottom = sprite.rect.top
                            self.direction.y = 0
                            self.on_ground = True
                            self.is_jumping = False  # Reset jumping state
                        else:
                            # Allow the player to pass through the platform when pressing down
                            self.hitbox_rect.bottom += 5  # Slightly move the player down to ensure they pass through
                            self.on_ground = False

    def animate(self, dt):
        if not self.alive:
            self.frame_index += ANIMATION_SPEED * dt
            if self.frame_index >= len(self.frames[self.state]):
                self.frame_index = len(self.frames[self.state]) - 1  # Stay on the last frame
        else:
            if self.attacking:
                self.frame_index += ANIMATION_SPEED * dt
                if self.frame_index >= len(self.frames[self.state]):
                    self.frame_index = 0
                    if self.on_ground:
                        self.state = 'idleSpriteAnim' if self.direction.x == 0 else 'walkSpriteAnim'
                    self.attacking = False
            else:
                self.frame_index += ANIMATION_SPEED * dt

        self.image = self.frames[self.state][int(self.frame_index % len(self.frames[self.state]))]
        self.image = self.image if self.facing_right else pygame.transform.flip(self.image, True, False)

    def get_state(self):
        if not self.alive:
            self.state = 'deathSpriteAnim'
        else:
            if self.attacking:
                if self.on_ground:
                    self.state = 'attackSpriteAnim'
                else:
                    self.state = 'jumpattackSpriteAnim'
            else:
                if self.on_ground:
                    if self.direction.x == 0:
                        self.state = 'idleSpriteAnim'
                    else:
                        self.state = 'walkSpriteAnim'
                else:
                    self.state = 'jumpSpriteAnim'

    def attack_check(self):
        if self.state in['attackSpriteAnim', 'jumpattackSpriteAnim']:
            for enemy in self.enemies:
                if self.hitbox_rect.colliderect(enemy.rect):
                    enemy.kill()

    def take_damage(self, amount):
        if not self.damage_cooldown.active:  # Only take damage if cooldown is not active
            self.current_health -= amount
            if self.current_health < 0:
                self.current_health = 0
            if self.current_health == 0 and self.alive:
                self.alive = False
                self.state = 'deathSpriteAnim'
                self.frame_index = 0
            self.damage_cooldown.activate()

    def death(self):
        if self.state == 'deathSpriteAnim' and self.frame_index >= len(self.frames[self.state]) - 1:
            pygame.quit()
            sys.exit()

    def update(self, dt):
        if self.alive:
            self.old_rect = self.rect.copy()
            self.input(dt)  # Pass dt to the input method
            self.move(dt)
            self.get_state()
            self.attack_check()
            self.animate(dt)
            self.damage_cooldown.update()
        else:
            self.animate(dt)
            self.death()
