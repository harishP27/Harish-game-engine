#This file was created by: Harish Purushothaman

#here we are importing libraries
import pygame as pg 
from settings import *
from sprites import *
import sys
from random import randint
from os import path


#here we are creating a game class
class Game:
    #defining what's in that class using a function
    def __init__(self):
        pg.init()
        #creating a setting for the game's graphics
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        #creating a title for the game
        pg.display.set_caption("My First Video Game")
        #using time to display game graphics such as frames per second (fps)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.running = True
        self.playing = True
        # used to store game info later on
        self.load_data()
    
    #TRANSPLANT
    def load_data(self):
        game_folder = path.dirname(__file__)
        self.map_data = []
        # 'r'     open for reading (default)
        # 'w'     open for writing, truncating the file first
        # 'x'     open for exclusive creation, failing if the file already exists
        # 'a'     open for writing, appending to the end of the file if it exists
        # 'b'     binary mode
        # 't'     text mode (default)
        # '+'     open a disk file for updating (reading and writing)
        # 'U'     universal newlines mode (deprecated)
        # below opens file for reading in text mode
        # with 
        '''
        The with statement is a context manager in Python. 
        It is used to ensure that a resource is properly closed or released 
        after it is used. This can help to prevent errors and leaks.
        '''
        with open(path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                print(line)
                self.map_data.append(line)
    
    def new(self):
        #variables for new sprites game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.objects = pg.sprite.Group()
        # self.player = Player(self, 10, 10)
        # self.all_sprites.add(self.player)
        #for x in range(10,20):
            #Wall(self, x, 5)
        #TRANSPLANT
        for row, tiles in enumerate(self.map_data):
            print(row)
            for col, tile in enumerate(tiles):
                print(col)
                if tile == 'x':
                    print("a wall at", row, col)
                    Wall(self, col, row)
                if tile == 'p':
                    self.player = Player(self, col, row)
                if tile == 'o':
                    Object(self, col, row)
       
    
    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            #this is the input
            self.events()
            #this is the processing
            self.update()
            #this is the output
            self.draw()

 
    
    def quit(self):
        pg.quit()
        sys.exit()
    #methods

        
    

    def input(self):
        pass
    def update(self):
        self.all_sprites.update()

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x,0), (x,HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0,y), (WIDTH, y))

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        pg.display.flip()

    def events(self):
            for event in pg.event.get():
                #when you hit the red x the game ends
                if event.type == pg.QUIT:
                    self.quit()
                    print("the game has ended...")
                #keyboard events
                # if event.type == pg.KEYDOWN:
                #     if event.key == pg.K_LEFT:
                #         self.player.move(dx = -1)
                # if event.type == pg.KEYDOWN:
                #     if event.key == pg.K_RIGHT:
                #         self.player.move(dx = 1)
                # if event.type == pg.KEYDOWN:
                #     if event.key == pg.K_UP:
                #         self.player.move(dy = -1)
                # if event.type == pg.KEYDOWN:
                #     if event.key == pg.K_DOWN:
                #         self.player.move(dy = 1)
                
    
    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass





    
    


#calling the class and run function and initiating the game
g = Game()
#g.show_go_screen()
while True:
    g.new()
    g.run()
    #g.show_go_screen()






