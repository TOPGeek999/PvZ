# Report <br><br>


## Introduction

### a. What is my application

The application that I made is a recreation of the hit game Plants vs. Zombies. So far, it is a much more basic, pixel version of it, where the player has to defend against waves of zombies by strategically placing various types of plants. The plants have different abilities, such as shooting projectiles or generating sun that works as the in-game currency. The goal of the game is to survive for as long as possible while fending off an increasingly challenging number of zombies.

The game features a grid-based layout where players can place plants, each with its own unique characteristics and abilities. As players progress through the game, they earn sunlight (which can be used for planting plants), manage their defenses, and strategically position plants to counter the advancing zombie hordes. Sound is also a feature in the game, as the goal was to make it resemble the original as closely as possible, so most of the sounds are the exact same as in Plants vs. Zombies <br><br>

### b. How to run my program

The program itself can be run either by launching the code through the command prompt (the application doesn't launch in Visual Studio as of now and I am working on fixing it) or by launching the executable file of the game (which is not included in the repository because of its size). <br><br>

### c. How to use my program

The program, or the game, is used and plays very similarly, if not identically to the core gameplay of Plants vs. Zombies itself. Once the application starts running, the player gets into action immediately.

First, he is greeted by the grid, which is the "board" of the game, used as the place for the plants to be planted on. It consists of a 9 by 5 set of tiles, of which every one can store a single plant at a time.

Right after the game starts, sun starts falling from the sky, that can be collected with a click of the left mouse button (holding it down and dragging across the falling sun also works). Then it can be used as currency to purchase seeds for the plants. The sun itself, as of now, falls down fairly slowly out of the screen, so the player has plenty of time to collect it.

On the right top corner, there are the 3 seed packets for the 3 plants: sunflower, peashooter and walnut. They can be purchased for their corresponding prices and planted on one of the empty tiles. The planting can be done by pressing on the seed packets to select them with the left mouse button and then placing them on one of the empty tiles. Selecting them could also be done by pressing the numbers 1, 2, or 3 on the keyboard.

The main enemy in this game is the zombies, that start to increasingly spawn, as more time passes. They deal damage to the plants by getting very near (being in the same time) and starting to eat them.

The plants themselves have different abilities that activate automatically. The sunflower produces the same exact sun that drops from the sky (the only difference is that it's much slower to drop down), the peashooter shoots peas that deal damage to the zombies and the walnut has a lot more health than the other plants, suited for defending the field.

Once the player dies, he can either press the ESC button to leave the game (can be done all the time) or can press the ENTER button to restart the game.<br><br><br>


## 2. Body/Analysis

### a. The explanation of how the program covers (implements) functional requirements

#### 1. Four Pillars of OOP:

- Polymorphism: The program utilizes polymorphism in various ways. For instance, different plant and zombie types have different behaviors. The update and draw methods in the Sunflower and Peashooter classes demonstrate polymorphic behavior based on the specific plant type.

Sunflower:

```py
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
```

Peashooter:

```py
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
```
<br>

- Abstraction: Abstraction is employed through the use of abstract methods and classes. The Plant class defines an abstract method update, which is implemented differently by its subclasses like Sunflower and Peashooter. This allows for a blueprint of behavior to be defined in the base class while allowing subclasses to provide concrete implementations.

Plant:

```py
def update(self, draw_pos):
        self.damage_cooldown -= 1
```

Sunflower:

```py
def update(self, draw_pos):
        self.cooldown -= random.random()*2
        if self.cooldown <= 0:
            self.game.projectiles.append(Sun(self.game, [draw_pos[0]+random.randint(-4,4), draw_pos[1]+16+random.randint(-2,2)], [0, 0.02], wave=False))
            self.cooldown = 780
        super().update(draw_pos)
```
<br>

- Inheritance: Inheritance is evident in the program through class inheritance. For instance, the Sunflower, Peashooter, and Walnut classes inherit from the Plant class. This allows them to inherit attributes and methods from the base class and define their own specific behaviors.

```py
class Walnut(Plant):
```
<br>

- Encapsulation: Encapsulation is utilized to encapsulate data and methods within classes. For example, attributes like game, type, and pos are encapsulated within the Plant class. This ensures that data is hidden and can only be accessed and modified through defined methods.

```py
class Plant:

    def __init__(self, game, type, pos, max_health):
        self.game = game
        self.type = type
        self.pos = pos
        self.img = game.assets["plants"][type]
        self.max_health = max_health
        self.health = max_health

        self.damage_cooldown = 30 <br><br>
```
<br><br>


#### 2. Design Patterns:

Factory Method Pattern: The program implements the Factory Method pattern with the PlantFactory and its concrete implementations such as SunflowerFactory, PeashooterFactory, and WalnutFactory. These factories encapsulate the creation logic for different types of plants, allowing the client code (Game class) to create plants without needing to know the specific plant types.

```py
class PlantFactory:
    def create_plant(self, game, plant_type, pos):
        raise NotImplementedError("Subclasses must implement create_plant method")

class SunflowerFactory(PlantFactory):
    def create_plant(self, game, pos):
        return Sunflower(game, pos)
        
def place_sunflower(self, pos):
        self.grid[pos[1]][pos[0]] = self.sunflower_factory.create_plant(self, pos)

self.place_sunflower((x, y))
```
<br><br>


#### 3. File I/O:

File I/O functionality is implemented in the program to import and export data. For instance, the program reads and writes data related to the sun timer from/to a file (sun_timer.txt). This functionality ensures that game progress, such as the state of the sun timer, can be saved and restored across sessions.

Reading from file:

```py
self.sun_timer_file = open("sun_timer.txt", "r")
self.sun_timer = int(float(self.sun_timer_file.read().strip()))
self.sun_timer_file.close()
```

Writing to file:

```py
self.sun_timer_file = open("sun_timer.txt", "w")
self.sun_timer_file.write(str(self.sun_timer))
self.sun_timer_file.close()
```
 <br><br><br>


## 3. Results and Summary

### a. Results

- The game covers almost all of the functional requirements, providing a playable Plants vs Zombies pixel recreation.

- The gameplay very closely resembles the original game, from its plant planting, zombies, all the way to the sound.

- Challenges during implementation included managing the complexity of the game logic, implementing certain functional requirements, making sure that the game itself worked in way that it needed to and making the pixel art look as similar as possible to the original game.

- Despite these challenges, the program achieves the desired functionality, demonstrating a solid understanding of OOP concepts and design patterns. The result is a functional game that provides an engaging user experience while mostly adhering to the specified requirements. <br><br>

### b. Conclusions

- The coursework has successfully demonstrated the implementation of OOP principles and design patterns in the development of a Plants vs Zombies recreation.

- The result is a functional game that allows players to engage in strategic gameplay by placing plants to defend against incoming waves of zombies. <br><br>


### c. The possible extention of my application

The possible extention of the program includes upgrades, such as an item, used to remove unwanted plants from the grid, improved visuals, additional plant and zombie types, improved user interface, level progression and so on.
