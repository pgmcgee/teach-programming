import pygame
from pygame.locals import *
import sys
import random
import time

class Character(object):
    def act(self):
        pass

    def draw(self):
        pass

    def position(self):
        pass

    def reset(self):
        pass

class Monster(Character):
    _image = 'images/monster.bmp'

    def __init__(self, game_map, position):
        self._load_surface()
        self._position = position

    def draw(self, screen):
        screen.blit(self._surface, _screen_pos_from_pos(self._position))

    def position(self):
        return self._position

    def _load_surface(self):
        self._surface = pygame.image.load(self._image).convert()
        self._surface.set_colorkey((0, 0, 0))

class Hero(Character):
    _images = {
        'left': 'images/zelda-left.bmp',
        'right': 'images/zelda-right.bmp',
        'up': 'images/zelda-up.bmp',
        'down': 'images/zelda-down.bmp'
    }
    _direction = 'right'
    _has_action = True

    def __init__(self, game_map, position):
        self._load_surfaces()
        self._load_map(game_map, position)

    def right(self):
        if not self._has_action:
            raise Exception("You don't have any actions left")
        if self._direction == 'up':
            self._direction = 'right'
        elif self._direction == 'right':
            self._direction = 'down'
        elif self._direction == 'down':
            self._direction = 'left'
        elif self._direction == 'left':
            self._direction = 'up'
        self._has_action = False

    def left(self):
        if not self._has_action:
            raise Exception("You don't have any actions left")
        if self._direction == 'up':
            self._direction = 'left'
        elif self._direction == 'left':
            self._direction = 'down'
        elif self._direction == 'down':
            self._direction = 'right'
        elif self._direction == 'right':
            self._direction = 'up'
        self._has_action = False

    def forward(self):
        if not self._has_action:
            raise Exception("You don't have any actions left")
        pos = self._current_position
        self._new_position(self._facing_position())
        self._has_action = False

    def feel(self):
        feeling = self._game_map.get(self._facing_position())
        if feeling == 'm':
            return 'monster'
        elif feeling == 'w':
            return 'wall'
        else:
            return 'empty'

    def attack(self):
        if not self._has_action:
            raise Exception("You don't have any actions left")
        attack_pos = self._facing_position()
        self._game_map.attack(attack_pos)
        self._has_action = False

    def act(self):
        pass

    def draw(self, screen):
        screen.blit(self._surfaces[self._direction],
                    _screen_pos_from_pos(self._current_position))

    def position(self):
        return self._current_position

    def reset(self):
        self._has_action = True

    def _facing_position(self):
        pos = self._current_position
        if self._direction == 'up':
            return (pos[0], pos[1]-1)
        elif self._direction == 'right':
            return (pos[0]+1, pos[1])
        elif self._direction == 'down':
            return (pos[0], pos[1]+1)
        elif self._direction == 'left':
            return (pos[0]-1, pos[1])

    def _new_position(self, position):
        if self._game_map.check_position(position):
            self._old_position = self._current_position
            self._current_position = position

    def _load_surfaces(self):
        self._surfaces = {}
        for direction, path in self._images.items():
            self._surfaces[direction] = pygame.image.load(path).convert()
            self._surfaces[direction].set_colorkey((0, 0, 0))

    def _load_map(self, game_map, position):
        self._game_map = game_map
        self._current_position = position

class Player(Hero):
    def act(self):
        if self.feel() == 'monster':
            self.attack()
        elif self.feel() == 'wall':
            self.right()
        else:
            self.forward()

class GameMap(object):
    _objects = []

    def __init__(self, game_map):
        self._load_map(game_map)
        self._load_objects()

    def check_position(self, pos):
        if pos[0] < 0 or pos[1] < 0:
            return False
        if pos[0] >= self.width or pos[1] >= self.height:
            return False
        return True

    def get(self, pos):
        """
        Values:
        - 'z': Hero (zelda)
        - 'w': Wall
        - 'm': Monster
        - 'x': Empty space
        """
        x, y = pos
        if self.check_position(pos):
            return self._game_map[y][x]
        else:
            return 'w'

    def attack(self, pos):
        if self.get(pos) == 'm':
            self._set(pos, 'x')
        for index, object in enumerate(self._objects):
            if object.position() == pos:
                self._objects.pop(index)

    def _set(self, pos, val):
        if val not in ('z', 'w', 'm', 'x'):
            return False
        x, y = pos
        if self.check_position(pos):
            self._game_map[y][x] = val
            return True
        return False

    def _load_map(self, game_map):
        self.width = len(game_map[0])
        self.height = len(game_map)

        self._game_map = []
        for y, row in enumerate(game_map):
            self._game_map.append([])
            for x, val in enumerate(row):
                self._game_map[y].append(val)

    def _load_objects(self):
        for y, row in enumerate(self._game_map):
            for x, val in enumerate(row):
                if val == 'z':
                    self._objects.append(Player(self, (x, y)))
                elif val == 'm':
                    self._objects.append(Monster(self, (x, y)))

    def act(self):
        for object in self._objects:
            object.act()

    def draw(self, screen):
        pygame.draw.rect(screen, COLORS['ground'], pygame.Rect((0, 0), screen_size))
        for object in self._objects:
            object.draw(screen)

    def reset(self):
        for object in self._objects:
            object.reset()

tile_size = (48, 48)
game_maps = [
    ["xxxmxx",
     "zxxxmx",
     "xxxxxm"],
]
current_game_map = game_maps[0]

print "Starting pygame..."
pygame.init()

print "Starting the game..."
screen_size = (tile_size[0]*len(current_game_map[0]), tile_size[1]*len(current_game_map))
screen = pygame.display.set_mode(screen_size)

print "Initializing the map..."
game_map = GameMap(game_maps[0])

print "Setting some configuration..."
pygame.key.set_repeat(1, 100)

print "Setting some constants..."
COLORS = {
    'ground': (30, 120, 60)
}

def _rect_from_pos(pos):
    return pygame.Rect(_screen_pos_from_pos(pos), tile_size)

def _screen_pos_from_pos(pos):
    return (tile_size[0]*pos[0], tile_size[1]*pos[1])

print "Running the loop..."
while 1:
    for event in pygame.event.get():
        if event.type == QUIT:
            print "I was told to quit, so I'm quitting"
            sys.exit()

    game_map.act()
    game_map.draw(screen)

    pygame.display.update()
    time.sleep(0.3)

    game_map.reset()
