import pygame, random, sys, json
from pygame.locals import *

sys.path.append('.\scripts')

from scripts.utilities import Projectile, Sun
from scripts.plants import Plant, Walnut
from scripts.zombies import Zombie

class Sunflower(Plant):

    def __init__(self, game, pos):
        super().__init__(game, "sunflower", pos, 8)
        self.cooldown = 120

    def update(self, draw_pos):
        self.cooldown -= random.random()*2
        if self.cooldown <= 0:
            self.game.projectiles.append(Sun(self.game, [draw_pos[0]+random.randint(-4,4), draw_pos[1]+16+random.randint(-2,2)], [0, 0.02], wave=False))
            self.cooldown = 780
        super().update(draw_pos)
    
    def draw(self, display, draw_pos):
        if self.cooldown <= 60:
            img_mask = pygame.mask.from_surface(self.img)
            img_mask = img_mask.to_surface()
            img_mask.set_colorkey((0,0,0))
            img_mask.set_alpha(30)
            super().draw(display, draw_pos)
            display.blit(img_mask ,draw_pos)
        else:
            super().draw(display, draw_pos)


class Peashooter(Plant):

    def __init__(self, game, pos):
        super().__init__(game, "peashooter", pos, 8)
        self.cooldown = 120

    def update(self, draw_pos):
        if self.game.zombie_lanes[self.pos[1]]:
            self.cooldown -= random.random()*2
            if self.cooldown <= 0:
                self.game.projectiles.append(Projectile(self.game, "pea", (draw_pos[0] + 10, draw_pos[1] + 15), [2, 0], 1))
                self.cooldown = 120
                random.choice(self.game.assets["sfx"]["throw"]).play()
        super().update(draw_pos)

    def draw(self, display, draw_pos):
        super().draw(display, draw_pos)


class PlantFactory:
    def create_plant(self, game, plant_type, pos):
        raise NotImplementedError("Subclasses must implement create_plant method")

class SunflowerFactory(PlantFactory):
    def create_plant(self, game, pos):
        return Sunflower(game, pos)

class PeashooterFactory(PlantFactory):
    def create_plant(self, game, pos):
        return Peashooter(game, pos)

class WalnutFactory(PlantFactory):
    def create_plant(self, game, pos):
        return Walnut(game, pos)


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.clock = pygame.time.Clock()

        self.window_size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        self.window = pygame.display.set_mode(self.window_size, FULLSCREEN|RESIZABLE)
        self.display = pygame.Surface((320, 180))

        self.sun_timer_file = open("sun_timer.txt", "r")

        self.sun_timer = int(float(self.sun_timer_file.read().strip()))

        self.sun_timer_file.close()

        self.sun_timer_file = open("sun_timer.txt", "w")

        self.assets = {
            "plants":{
                "sunflower":pygame.image.load("data/Images/Plants/sunflower.png"),
                "peashooter":pygame.image.load("data/Images/Plants/peashooter.png"),
                "walnut":[pygame.image.load("data/images/plants/walnut.png").subsurface((0,0,16,32)),
                          pygame.image.load("data/images/plants/walnut.png").subsurface((16,0,16,32)),
                          pygame.image.load("data/images/plants/walnut.png").subsurface((32,0,16,32))]
            },
            "seeds":{
                "sunflower":pygame.image.load("data/Images/Seeds/sunflower.png"),
                "peashooter":pygame.image.load("data/Images/Seeds/peashooter.png"),
                "walnut":pygame.image.load("data/Images/Seeds/walnut.png")
            },
            "zombies":{
                "normal":pygame.image.load("data/Images/Zombies/zombie.png")
            },
            "projectiles":{
                "pea":pygame.image.load("data/Images/projectiles/pea.png")
            },
            "sun":pygame.image.load("data/Images/sun.png"),
            "sfx":{
                "splat":[pygame.mixer.Sound("data/Sounds/splat.ogg"),
                         pygame.mixer.Sound("data/Sounds/splat2.ogg"),
                         pygame.mixer.Sound("data/Sounds/splat3.ogg")],
                "plant":[pygame.mixer.Sound("data/Sounds/plant.ogg"),
                         pygame.mixer.Sound("data/Sounds/plant2.ogg")],
                "gulp":pygame.mixer.Sound("data/Sounds/gulp.ogg"),
                "swing":pygame.mixer.Sound("data/Sounds/swing.ogg"),
                "shoop":pygame.mixer.Sound("data/Sounds/shoop.ogg"),
                "chomp":[pygame.mixer.Sound("data/Sounds/chomp.ogg"),
                         pygame.mixer.Sound("data/Sounds/chomp2.ogg"),
                         pygame.mixer.Sound("data/Sounds/chomp3.mp3"),
                         pygame.mixer.Sound("data/Sounds/chomp4.mp3")],
                "throw":[pygame.mixer.Sound("data/Sounds/throw.ogg"),
                         pygame.mixer.Sound("data/Sounds/throw2.ogg")],
                "losemusic":pygame.mixer.Sound("data/Sounds/losemusic.ogg"),
                "losescream":pygame.mixer.Sound("data/Sounds/scream.ogg"),
                "seedlift":pygame.mixer.Sound("data/Sounds/seedlift.ogg"),
                "buzzer":pygame.mixer.Sound("data/Sounds/buzzer.ogg"),
                "points":pygame.mixer.Sound("data/Sounds/points.ogg")
            }
        }
        
        self.font16 = pygame.font.Font("data/m6x11.ttf", 16)
        self.font32 = pygame.font.Font("data/m6x11.ttf", 32)
        self.font48 = pygame.font.Font("data/m6x11.ttf", 48)

        self.sunflower_factory = SunflowerFactory()
        self.peashooter_factory = PeashooterFactory()
        self.walnut_factory = WalnutFactory()


    def run(self):
        running = True

        self.cur_plant = ""

        self.mouse_pos = (0,0)

        self.grid = [[0,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0,0]]

        self.entities = []
        self.particles = []
        self.projectiles = []
        self.zombies = []
        self.zombie_lanes = [False, False, False, False, False]
        
        pygame.mixer.music.load("data/Music/grasswalk.mp3")
        pygame.mixer.music.play(-1, 0, 100)
        pygame.mixer.music.set_volume(0.4)

        self.level_timer = 0

        self.zombie_time = 600
        self.zombie_timer = 600
        self.zombie_max = 1
        self.zombie_max_limit = 10
        self.zombie_last_lane = 5

        self.sun = 50
        self.sun_time = 720
        self.sun_timer = 120

        self.seed_collider_1 = pygame.Rect(292, 4, 24, 32)
        self.seed_collider_2 = pygame.Rect(264, 4, 24, 32)
        self.seed_collider_3 = pygame.Rect(236, 4, 24, 32)

        while running:
            self.display.fill((0,0,0))

            self.mouse_pos = pygame.mouse.get_pos()
            self.mouse_pos = (self.mouse_pos[0]*(320/self.window_size[0]), self.mouse_pos[1]*(180/self.window_size[1]))

            self.level_timer += 1

            self.zombie_timer -= 1 + (random.random()-0.5)
            if self.zombie_timer <= 0:

                if self.zombie_time >= 30:
                    self.zombie_time -= 20
                self.zombie_timer = self.zombie_time

                if len(self.zombies) < self.zombie_max:
                    lanes = [0,1,2,3,4]
                    try:
                        lanes.remove(self.zombie_last_lane)
                    except:
                        pass
                    lane = random.choice(lanes)
                    self.zombie_last_lane = lane
                    self.zombies.append(Zombie(self, "normal", lane))
            if (self.level_timer%2400) == 0 and self.zombie_max < self.zombie_max_limit:
                self.zombie_max += 1

            self.sun_timer -= 1 + (random.random()-0.5)
            if self.sun_timer <= 0:
                self.sun_timer = self.sun_time
                self.projectiles.append(Sun(self, [random.randint(40, 260),-19], [0, 0.1]))

            self.sun_timer_file.seek(0)
            self.sun_timer_file.write(str(self.sun_timer))
            self.sun_timer_file.truncate()

            y = 0
            for row in self.grid:
                x = 0
                for tile in row:
                    tile_rect = pygame.Rect((x*24) + 52, (y*24) + 46, 24, 24)
                    pygame.draw.rect(self.display, (10+(10*((x+y)%2)),10+(10*((x+y)%2)),10+(10*((x+y)%2))), tile_rect)
                    
                    if tile != 0:
                        tile.update(((x*24) + 54 + 2, (y*24) + 48 - 12))
                        tile.draw(self.display, ((x*24) + 54 + 2, (y*24) + 48 - 12))

                        if tile.health <= 0:
                            self.grid[y][x] = 0
                            self.assets["sfx"]["gulp"].play()

                    if self.cur_plant != "":
                        try:
                            plant_overlay = pygame.Surface(self.assets["plants"][self.cur_plant].get_size())
                        except:
                            plant_overlay = pygame.Surface(self.assets["plants"][self.cur_plant][0].get_size())
                        plant_overlay.set_colorkey((0,0,0))
                        try:
                            plant_overlay.blit(self.assets["plants"][self.cur_plant], (0,0))
                        except:
                            plant_overlay.blit(self.assets["plants"][self.cur_plant][0], (0,0))
                        self.display.blit(plant_overlay, (self.mouse_pos[0]-8, self.mouse_pos[1]-24))

                    if tile_rect.collidepoint(self.mouse_pos[0], self.mouse_pos[1]) and tile == 0 and self.cur_plant != "":
                        plant_overlay.set_alpha(40)
                        self.display.blit(plant_overlay, ((x*24) + 54 + 2, (y*24) + 48 - 12))
                        if pygame.mouse.get_pressed()[0]:
                            if self.cur_plant == "sunflower":
                                self.sun -= 50
                                self.place_sunflower((x, y))
                                random.choice(self.assets["sfx"]["plant"]).play()
                            if self.cur_plant == "peashooter":
                                self.sun -= 100
                                self.place_peashooter((x, y))
                                random.choice(self.assets["sfx"]["plant"]).play()
                            if self.cur_plant == "walnut":
                                self.sun -= 50
                                self.place_walnut((x, y))
                                random.choice(self.assets["sfx"]["plant"]).play()
                            self.cur_plant = ""

                    x += 1
                y += 1

            self.entities = self.projectiles + self.zombies

            self.zombie_lanes = [False, False, False, False, False]
            for i, zombie in sorted(enumerate(self.zombies), reverse=True):
                zombie.update()
                zombie.draw(self.display)
                self.zombie_lanes[zombie.lane] = True
                for a, projectile in sorted(enumerate(self.projectiles), reverse=True):
                    if isinstance(projectile, Projectile):
                        if zombie.rect().colliderect(projectile.rect()):
                            zombie.health -= projectile.damage
                            self.projectiles.pop(a)
                            random.choice(self.assets["sfx"]["splat"]).play()
                if zombie.health <= 0:
                    self.zombies.pop(i)
                if zombie.pos[0] <= 4:
                    self.dead(zombie)

            for i, projectile in sorted(enumerate(self.projectiles), reverse=True):
                projectile.update()
                projectile.draw(self.display)
                if -32 > projectile.pos[0] > 352 or -32 > projectile.pos[1] > 212:
                    self.projectiles.pop(i)
                if isinstance(projectile, Sun):
                    if projectile.rect().collidepoint(self.mouse_pos) and pygame.mouse.get_pressed()[0]:
                        self.projectiles.pop(i)
                        self.sun += projectile.value
                        self.assets["sfx"]["points"].play()

            for particle in self.particles:
                particle.update()
                particle.draw(self.display)

            self.display.blit(self.assets["sun"], (4,4))
            self.display.blit(self.font16.render("{:,}".format(self.sun), False, (255,255,255)), (4+19+4,8))

            '''
            self.display.blit(self.font16.render("Max Zombies : "+"{:,}".format(self.zombie_max), False, (255,255,255)), (4,8+16))
            self.display.blit(self.font16.render("Zombie Time : "+"{:,}".format(self.zombie_time), False, (255,255,255)), (4,8+32))
            self.display.blit(self.font16.render("Zombie Count : "+"{:,}".format(len(self.zombies)), False, (255,255,255)), (4,8+48))
            self.display.blit(self.font16.render("Level Timer : "+"{:,}".format(self.level_timer) + " ; " + str(self.level_timer%1200), False, (255,255,255)), (4,8+64))
            '''

            self.display.blit(self.assets["seeds"]["sunflower"], (236, 4))
            self.display.blit(self.assets["seeds"]["peashooter"], (264, 4))
            self.display.blit(self.assets["seeds"]["walnut"], (292, 4))

            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_1:
                        self.cur_plant = "sunflower"
                    if event.key == K_2:
                        self.cur_plant = "peashooter"
                    if event.key == K_3:
                        self.cur_plant = "walnut"
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.seed_collider_1.collidepoint(self.mouse_pos[0], self.mouse_pos[1]):
                            if self.sun >= 50:
                                self.cur_plant = "walnut"
                                self.assets["sfx"]["seedlift"].play()
                            else:
                                self.assets["sfx"]["buzzer"].play()
                        if self.seed_collider_2.collidepoint(self.mouse_pos[0], self.mouse_pos[1]):
                            if self.sun >= 100:
                                self.cur_plant = "peashooter"
                                self.assets["sfx"]["seedlift"].play()
                            else:
                                self.assets["sfx"]["buzzer"].play()
                        if self.seed_collider_3.collidepoint(self.mouse_pos[0], self.mouse_pos[1]):
                            if self.sun >= 50:
                                self.cur_plant = "sunflower"
                                self.assets["sfx"]["seedlift"].play()
                            else:
                                self.assets["sfx"]["buzzer"].play()

                    if event.button == 3:
                        self.cur_plant = ""
            
            self.window.blit(pygame.transform.scale(self.display, self.window_size), (0,0))
            pygame.display.update()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()


    def place_sunflower(self, pos):
        self.grid[pos[1]][pos[0]] = self.sunflower_factory.create_plant(self, pos)

    def place_peashooter(self, pos):
        self.grid[pos[1]][pos[0]] = self.peashooter_factory.create_plant(self, pos)

    def place_walnut(self, pos):
        self.grid[pos[1]][pos[0]] = self.walnut_factory.create_plant(self, pos)

    def dead(self, zombie):
            running = True
            dead_black = pygame.Surface(self.display.get_size())
            dead_black.set_alpha(2)

            dead_text_1 = self.font32.render("THE ZOMBIES", False, (50, 255, 50))
            dead_text_1_rect = dead_text_1.get_rect()
            dead_text_1_rect.centerx = 160

            dead_text_2 = self.font32.render("ATE YOUR", False, (50, 255, 50))
            dead_text_2_rect = dead_text_2.get_rect()
            dead_text_2_rect.centerx = 160
            dead_text_2_rect.centery = 90

            dead_text_1_rect.bottom = dead_text_2_rect.top

            dead_text_3 = self.font48.render("BRAINS!", False, (50, 255, 50))
            dead_text_3_rect = dead_text_3.get_rect()
            dead_text_3_rect.centerx = 160
            dead_text_3_rect.top = dead_text_2_rect.bottom

            self.timer = 0

            pygame.mixer.music.fadeout(100)

            while running:
                self.timer += 1

                self.display.blit(dead_black, (0,0))
                zombie.draw(self.display)

                if self.timer == 20:
                    self.assets["sfx"]["losemusic"].play()
                if self.timer == 240:
                    self.assets["sfx"]["chomp"][0].play()
                if self.timer == 280:
                    self.assets["sfx"]["chomp"][1].play()
                if self.timer == 300:
                    self.assets["sfx"]["losescream"].play()
                if self.timer >= 330:
                    self.display.blit(dead_text_1, dead_text_1_rect)
                    self.display.blit(dead_text_2, dead_text_2_rect)
                    self.display.blit(dead_text_3, dead_text_3_rect)

                for event in pygame.event.get():
                    if event.type == QUIT:
                        running = False
                    if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            running = False
                        if event.key == K_RETURN:
                            self.run()

                self.window.blit(pygame.transform.scale(self.display, self.window_size), (0,0))
                pygame.display.update()
                self.clock.tick(60)


            self.sun_timer_file.close()
            pygame.quit()
            sys.exit()


Game().run()
input()