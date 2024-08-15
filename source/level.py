from settings import *
from sprites import Sprite, AnimatedSprite
from player import Player
from groups import AllSprites
from enemies import Zombie, SkeletonArcher, Arrow
from support import *

class Level:
    def __init__(self, tmx_map, level_frames):
        self.display_surface = pygame.display.get_surface()

        self.all_sprites = AllSprites()
        self.floor_sprites = pygame.sprite.Group()
        self.platform_sprites = pygame.sprite.Group()
        self.damage_sprites = pygame.sprite.Group()
        self.zombie_sprites = pygame.sprite.Group()
        self.skeletonarcher_sprites = pygame.sprite.Group()
        self.arrow_sprite = pygame.sprite.Group()

        # Call the setup method to initialize the map and player
        self.setup(tmx_map, level_frames)
        self.arrow_surf = level_frames['arrow']

    def setup(self, tmx_map, level_frames, animation_speed = ANIMATION_SPEED):
        # map
        for layer in ['Backdrop','Details','Floor','Platform']:
            if layer == 'Floor':
                for x, y, surf in tmx_map.get_layer_by_name('Floor').tiles():
                    Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, (self.all_sprites, self.floor_sprites))
            elif layer == 'Platform':
                for x, y, surf in tmx_map.get_layer_by_name('Platform').tiles():
                    Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, (self.all_sprites, self.platform_sprites))
            else:     
                for x, y, surf in tmx_map.get_layer_by_name(layer).tiles():
                    Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, (self.all_sprites))

        # tiles
        for obj_layer in ['MiscObj','Point']:
            object_layer = tmx_map.get_layer_by_name(obj_layer)
            for obj in object_layer:
                if obj.name == 'end_point':
                    self.end_point = Sprite(
                        pos=(obj.x, obj.y),
                        surf= import_image('..','assets','sprites','Medieval_Castle_Asset_Pack','Decorations','door'),
                        groups=self.all_sprites)
                else:
                    frames = level_frames[obj.name]
                    AnimatedSprite((obj.x, obj.y), frames, self.all_sprites, animation_speed)

        # player character
        for obj in tmx_map.get_layer_by_name('Char'):
            if obj.name == 'playerChar':
                self.player = Player(
                    pos = (obj.x, obj.y),
                    groups = self.all_sprites,
                    floor_sprites = self.floor_sprites,
                    platform_sprites = self.platform_sprites,
                    frames = level_frames['player'])
                self.player.enemies = self.damage_sprites

        # enemies
        for obj in tmx_map.get_layer_by_name('Enemy'):
            if obj.name == 'Zombie':
                Zombie(
                    pos = (obj.x, obj.y),
                    frames = level_frames['Zombie'],
                    groups = (self.all_sprites, self.damage_sprites, self.zombie_sprites),  # Pass the tuple as a keyword argument
                    floor_sprites = self.floor_sprites,
                    platform_sprites = self.platform_sprites)
            if obj.name == 'SkeletonArcher':
                SkeletonArcher(
                    pos = (obj.x, obj.y),
                    frames = level_frames['SkeletonArcher'],
                    groups = (self.all_sprites, self.damage_sprites, self.skeletonarcher_sprites),
                    floor_sprites = self.floor_sprites,
                    platform_sprites = self.platform_sprites,
                    player = self.player,
                    arrow = self.arrow)

    def arrow(self, pos, direction):
        Arrow(pos, (self.all_sprites, self.damage_sprites, self.arrow_sprite), self.arrow_surf, direction, 100, self.floor_sprites, self.platform_sprites, self.player)

    def hurt_player(self):
        for sprite in self.damage_sprites:
            if sprite.rect.colliderect(self.player.hitbox_rect):
                if isinstance(sprite, Arrow):
                    sprite.kill()  
                    self.player.take_damage(10) 
                elif isinstance(sprite, Zombie):
                    self.player.take_damage(10) 
                elif isinstance(sprite, SkeletonArcher):
                    self.player.take_damage(10)

    def draw_health_bar(self, surface, pos, size, border_color, fill_color, health_percentage):
        border_rect = pygame.Rect(pos, size)
        fill_rect = pygame.Rect(pos, (size[0] * health_percentage, size[1]))
        pygame.draw.rect(surface, border_color, border_rect, 2)
        pygame.draw.rect(surface, fill_color, fill_rect)

    def check_level_complete(self):
        if self.player.hitbox_rect.colliderect(self.end_point.rect):
            self.level_complete()

    def level_complete(self):
        print("Game complete!")  # actual level completion animation?
        pygame.quit()
        sys.exit()

    def run(self, dt):
        self.all_sprites.update(dt)
        self.display_surface.fill('black')
        self.hurt_player()
        self.check_level_complete()
        self.all_sprites.draw(self.player.rect.center)
        health_percentage = self.player.current_health / self.player.max_health
        self.draw_health_bar(self.display_surface, (10, 10), (200, 20), (255, 255, 255), (255, 0, 0), health_percentage)
