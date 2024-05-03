# This file was created by: Harish P


import pygame as pg
from settings import *
from random import choice
from random import randint
import sys
from os import path

# write a player class



dir = path.dirname(__file__)
img_dir = path.join(dir, 'images')


# sets up file with multiple images...
class Spritesheet:
    # utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        # grab an image out of a larger spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        # image = pg.transform.scale(image, (width, height))
        image = pg.transform.scale(image, (width * 4, height * 4))
        return image
    
def draw_shield_bar(shield, surface, x, y):
        if shield < 0:
            shield = 0
        BAR_LENGTH = 64
        BAR_HEIGHT = 32
        fill = (shield/100) * BAR_LENGTH
        outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
        pg.draw.rect(surface, BLUE, outline_rect, 1)
        pg.draw.rect(surface, GREEN, fill_rect)
    
class Shield(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h, center, pct):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        #pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface([w, h])  # Adjusted size for the shield
        #self.image.set_colorkey(BLACK)  # Set transparent background
        self.image.fill(GREEN)  # Fill with white color (adjust as needed)
        #pg.draw.circle(self.image, BLUE, (16, 16), 16)  # Draw a blue circle (adjust as needed)
        self.rect = self.image.get_rect()
        #self.player = player
        self.rect.x = x
        self.rect.y = y
        self.center = center
        self.pct = pct

    def update(self):
        self.rect.x = self.center.rect.x
        self.rect.y = self.center.rect.y



    



class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        #self.player = player
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = game.player_img
        #self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (512,384)
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.moneybag = 0
        self.speed = 300
        self.hitpoints = 100
        #self.shield = 100
        self.healthbar = Shield(self.game, self.rect.x, self.rect.y, self.rect.w, 5, self, self.hitpoints)
        self.running = True

    def death(self):
        self.x = self.game.p1col * TILESIZE
        self.y = self.game.p1row * TILESIZE
        print("You died")

    

    
    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -self.speed
            print(self.rect.x)
            print(self.rect.y)
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = self.speed
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -self.speed
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = self.speed
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071
            
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False )
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False )
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y

   
    # def move(self, dx=0, dy=0):
    #     self.x += dx
    #     self.y += dy

    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "PowerUp":
                print(hits[0].__class__.__name__)
                self.speed += 1000
    # UPDATE THE UPDATE
    def update(self):
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        # add collision later
        self.collide_with_walls('x')
        self.rect.y = self.y
        # add collision later
        self.collide_with_walls('y')
        self.collide_with_group(self.game.coins, True)
        self.collide_with_group(self.game.power_ups, True)
        # I made it so that you collide with enemy the same way you collide with a coin. 
        self.collide_with_group(self.game.mobs, True)
        self.collide_with_group(self.game.spikes, True)
        


# 
# 
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == 'Mob':
                print("you died")
                self.hitpoints -= 34
                # pg.quit()
                # sys.exit()
            if str(hits[0].__class__.__name__) == "Coin":
                print("coin")
                self.moneybag += 1
            if str(hits[0].__class__.__name__) == "PowerUp":
                print("speed boost")
                self.speed += 150
            if str(hits[0].__class__.__name__) == "Spike":
                print("oof")
                self.speed -= 150
            if str(hits[0].__class__.__name__) == "Mob2":
                print("You lost")
                sys.exit()
            #if str(hits[0].__class__.__name__) == "Mob":
                #print("ok")
                self.hitpoints -= 10
            if self.moneybag == 12:
                sys.exit()
                print("You won")

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.lights_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.speed = 0
    def update(self):
        # self.rect.x += 1
        self.rect.x += TILESIZE * self.speed
        # self.rect.y += TILESIZE * self.speed
        if self.rect.x > WIDTH or self.rect.x < 0:
            self.speed *= -1
        # if self.rect.y > HEIGHT or self.rect.y < 0:
        #     self.speed *= -1

class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        #self.image = pg.Surface((TILESIZE, TILESIZE))
        #self.image.fill(RED)
        self.image = self.game.mob_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.vx, self.vy = 100, 100
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.speed = 300
        
    def collide_with_walls(self, dir):
        if dir == 'x':
            # print('colliding on the x')
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                self.vx *= -1
                self.rect.x = self.x
        if dir == 'y':
            # print('colliding on the y')
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                self.vy *= -1
                self.rect.y = self.y
    def update(self):
        
        # self.image.blit(self.game.screen, self.pic)
        # pass
        # # self.rect.x += 1
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        if self.rect.x < self.game.player.rect.x:
            self.vx = 100
        if self.rect.x > self.game.player.rect.x:
            self.vx = -100    
        if self.rect.y < self.game.player.rect.y:
            self.vy = 100
        if self.rect.y > self.game.player.rect.y:
            self.vy = -100
        self.rect.x = self.x
        #self.collide_with_walls('x')
        self.rect.y = self.y
        #self.collide_with_walls('y')

class Coin(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.coins
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.coin_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class PowerUp(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.power_ups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.chicken_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

#defining a new spike class
class Spike(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.spikes
        #below calling the super class
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.spike_img
        #getting imported image through rect
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


    
        



class Mob2(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.mob2_img
        #self.image = pg.Surface((TILESIZE, TILESIZE))
        #self.image.fill(RED)
        self.rect = self.image.get_rect()
        #self.x = x
        #self.y = y
        self.vx, self.vy = 100, 100
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.speed = 150

    def collide_with_walls(self, dir):
        if dir == 'x':
            # print('colliding on the x')
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                self.vx *= -1
                self.rect.x = self.x
        if dir == 'y':
            # print('colliding on the y')
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                self.vy *= -1
                self.rect.y = self.y
    def update(self):
        # self.rect.x += 1
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt

        if self.rect.x < self.game.player.rect.x:
            self.vx = 100
        if self.rect.x > self.game.player.rect.x:
            self.vx = -100    
        if self.rect.y < self.game.player.rect.y:
            self.vy = 100
        if self.rect.y > self.game.player.rect.y:
            self.vy = -100
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')
















        
    
    

        
      

        
        

    


