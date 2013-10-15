import pygame
from pygame.locals import *
import sys

print "Starting the game..."
screen = pygame.display.set_mode((640, 480))

print "Setting some configuration..."
pygame.key.set_repeat(1, 100)

print "Loading the image..."
player_image = pygame.image.load('cat.bmp').convert()
player_image.set_colorkey((255, 255, 255))

print "Drawing the background..."
pygame.draw.rect(screen, (30, 120, 60), pygame.Rect(0, 360+player_image.get_height(), 640, 120))
pygame.draw.rect(screen, (60, 90, 180), pygame.Rect(0, 0, 640, 360+player_image.get_height()))

print "Loading the player actions..."
class Player:
    def __init__(self, surface, position):
        self.surface = surface
        self.old_position = position
        self.position = position
        self.size = (self.surface.get_width(), self.surface.get_height())
        self.draw()

    def draw(self):
        pygame.draw.rect(screen, (60, 90, 180), self.old_position_rect())
        screen.blit(self.surface, self.position)

    def move(self, amount):
        if self.position[0] + amount < 0 or self.position[0] + amount > 480:
            return
        self.old_position = self.position
        self.position = (self.position[0] + amount, self.position[1])
        self.draw()

    def old_position_rect(self):
        return pygame.Rect(self.old_position[0], self.old_position[1], self.size[0], self.size[1])

print "Creating a player..."
player = Player(player_image, (0, 360))

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

    print "Updating the screen..."
    pygame.display.update()
