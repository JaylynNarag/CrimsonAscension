from settings import *
from level import Level
from pytmx.util_pygame import load_pygame
from os.path import join
from support import *

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Crimson Ascension')
        self.clock = pygame.time.Clock()
        self.import_assets()

        self.tmx_maps = {0: load_pygame(join('..', 'assets', 'maps', 'dungeonlvlmap.tmx'))}
        self.current_stage = Level(self.tmx_maps[0], self.level_frames)

    def import_assets(self): # use import sub folders to extract mass animations? - fix later
        self.level_frames = {
            'torch_big_blue': import_folder('..','assets','sprites','Medieval_Castle_Asset_Pack','Decorations','Animated Decorations','torch_big_blue'),
            'chest': import_image('..','assets','sprites','Medieval_Castle_Asset_Pack','Decorations','Animated Decorations','chest','chest_1'),
            'candelabrum_tall': import_folder('..','assets','sprites','Medieval_Castle_Asset_Pack','Decorations','Animated Decorations','candelabrum_tall'),
            'Zombie': import_folder('..','assets','sprites','enemiesAnim','Zombie'),
            'SkeletonArcher': import_sub_folders('..','assets','sprites','enemiesAnim','SkeletonArcher'),
            'torch_big': import_folder('..','assets','sprites','Medieval_Castle_Asset_Pack','Decorations','Animated Decorations','torch_big'),
            'door': import_image('..','assets','sprites','Medieval_Castle_Asset_Pack','Decorations','door'),
            'weapon_rack': import_image('..','assets','sprites','Medieval_Castle_Asset_Pack','Decorations','weapon_rack'),
            'sword_1': import_image('..','assets','sprites','Medieval_Castle_Asset_Pack','Decorations','sword_1'),
            'sword_2': import_image('..','assets','sprites','Medieval_Castle_Asset_Pack','Decorations','sword_2'),
            'pole_axe': import_image('..','assets','sprites','Medieval_Castle_Asset_Pack','Decorations','pole_axe'),
            'axe': import_image('..','assets','sprites','Medieval_Castle_Asset_Pack','Decorations','axe'),
            'bookshelf_1': import_image('..','assets','sprites','Medieval_Castle_Asset_Pack','Decorations','bookshelf_1'),
            'bookshelf_2': import_image('..','assets','sprites','Medieval_Castle_Asset_Pack','Decorations','bookshelf_2'),
            'arrow': import_image('..','assets','sprites','enemiesAnim','misc','tile000'),
            'player': import_sub_folders('..','assets','sprites','playerAnim')
            }

    def run(self):
        fps = 60  # Set your desired FPS
        while True:
            dt = self.clock.tick(fps) / 1000  # Lock frame rate and calculate dt
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.current_stage.run(dt)
            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()
