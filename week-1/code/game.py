import pygame
from pygame.locals import *
import sys
import random

print "Starting pygame..."
pygame.init()

print "Starting the game..."
screen = pygame.display.set_mode((640, 480))

print "Setting some configuration..."
pygame.key.set_repeat(1, 100)

print "Loading the player image..."
player_image = pygame.image.load('cat.bmp').convert()
player_image.set_colorkey((255, 255, 255))

print "Loading the bird image..."
bird_image = pygame.image.load('bird.bmp').convert()
bird_image.set_colorkey((255, 255, 255))

print "Loading colors..."
sky_color = (60, 90, 180)
ground_color = (30, 120, 60)

print "Drawing the background..."
pygame.draw.rect(screen, ground_color, pygame.Rect(0, 360+player_image.get_height(), 640, 120))
pygame.draw.rect(screen, sky_color, pygame.Rect(0, 0, 640, 360+player_image.get_height()))

print "Loading the general action..."
class Agent(object):
    def __init__(self, surface, position):
        self.surface = surface
        self.old_position = position
        self.position = position
        self.size = (self.surface.get_width(), self.surface.get_height())
        self.draw()

    def undraw(self):
        pygame.draw.rect(screen, sky_color, self.old_position_rect())

    def draw(self, undraw=True):
        if undraw:
            self.undraw()
        screen.blit(self.surface, self.position)

    def min_position(self):
        return 0

    def move(self, amount, undraw=True):
        if self.position[0] + amount < self.min_position():
            self.position = (0, self.position[1])
            return

        if self.position < 640-self.size[0] and self.position[0] + amount > 640-self.size[0]:
            self.position = (640-self.size[0], self.position[1])
            return

        self.old_position = self.position
        self.position = (self.position[0] + amount, self.position[1])
        self.draw(undraw)

    def position_rect(self):
        return pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])

    def old_position_rect(self):
        return pygame.Rect(self.old_position[0], self.old_position[1], self.size[0], self.size[1])

print "Loading the player actions..."
class Player(Agent):
    pass

print "Loading the bird actions..."
class Bird(Agent):
    def __init__(self, surface, time):
        position = (620, random.randrange(20, 240))
        self.speed = random.randrange(50, 100) / 10.0
        self.time = time
        self.old_time = time
        super(Bird, self).__init__(surface, position)

    def move_autonomously(self, time):
        time_difference = time - self.time
        self.move(-time_difference/self.speed, False)
        self.old_time = self.time
        self.time = time

    def min_position(self):
        return -300

    def is_done(self):
        return self.position[0] < -100

    def remove(self):
        self.undraw()
        pygame.draw.rect(screen, sky_color, self.position_rect())

print "Loading the laser actions..."
class Laser(Agent):
    def __init__(self, cat_position, time):
        position = (cat_position[0]+41, cat_position[1]-5)
        surface = pygame.Surface((2, 20))
        surface.fill((255, 0, 0))
        self.time = time
        self.old_time = time
        super(Laser, self).__init__(surface, position)

    def move(self, amount, undraw=True):
        self.old_position = self.position
        self.position = (self.position[0], self.position[1] - amount)
        self.draw(undraw)

    def is_done(self):
        return self.position[1] < -60

    def move_autonomously(self, time):
        time_difference = time - self.time
        self.move(time_difference, False)
        self.old_time = self.time
        self.time = time

    def remove(self):
        self.undraw()
        pygame.draw.rect(screen, sky_color, self.position_rect())

print "Loading the scoring actions..."
class Score(object):
    def __init__(self):
        self.position = (420, 450)
        self.score = 0
        self.draw()

    def add_kill(self):
        self.score += 1

    def draw(self):
        font = pygame.font.Font(None, 36)
        text = font.render("Birds Killed: " + str(self.score), True, (255, 255, 255))
        text_position = text.get_rect()
        text_position.left = self.position[0]
        text_position.top = self.position[1]
        pygame.draw.rect(screen, ground_color, text_position)
        screen.blit(text, self.position)

print "Creating a player..."
player = Player(player_image, (0, 360))

print "Creating the list of birds..."
birds = []

print "Creating the list of lasers..."
lasers = []

print "Creating the score..."
score = Score()

def remove_bird(bird):
    bird.remove()
    birds.remove(bird)

def remove_laser(laser):
    laser.remove()
    lasers.remove(laser)

print "Running the loop..."
while 1:
    for event in pygame.event.get():
        if event.type in (QUIT,):
            print "I was told to quit, so I'm quitting"
            sys.exit()
        if event.type in (KEYDOWN,):
            if event.key == K_q:
                print "You pressed the 'q' key, so I'm quitting"
                sys.exit()
            if event.key == K_RIGHT:
                print "You press the right arrow, so I'll move the player to the right"
                player.move(10)
            if event.key == K_LEFT:
                print "You press the left arrow, so I'll move the player to the left"
                player.move(-10)
            if event.key == K_UP:
                print "You pressed the up arrow, so I'll fire a laser"
                lasers.append(Laser(player.position, pygame.time.get_ticks()))

    print "Erasing birds and lasers..."
    # Undraw all the birds and lasers first so that the removal method doesn't draw over new birds
    for bird in birds:
        bird.undraw()
    for laser in lasers:
        laser.undraw()

    print "Moving all the birds..."
    for bird in birds:
        bird.move_autonomously(pygame.time.get_ticks())
        if bird.is_done():
            remove_bird(bird)

    print "Moving all the lasers..."
    for laser in lasers:
        laser.move_autonomously(pygame.time.get_ticks())
        if laser.is_done():
            remove_laser(laser)

    print "Checking for collisions..."
    for bird in birds:
        for laser in lasers:
            if bird.position_rect().colliderect(laser.position_rect()):
                remove_bird(bird)
                remove_laser(laser)
                score.add_kill()
                score.draw()

    if random.randrange(0, 20) == 0:
        print "Adding a bird"
        birds.append(Bird(bird_image, pygame.time.get_ticks()))

    print "Updating the screen..."
    pygame.display.update()
