import pygame,sys
import libs.pgt as pgt
from libs.pgt import Vector2
from enum import Enum
import assetsloader as res

# Global config
BASESCREEN_WIDTH = 256 
BASESCREEN_HEIGHT = 240
WINDOW_SCALE = 2
GAME_SPEED = 60
TITLE = "Kirbo Engine"

# player state
class PlayerState(Enum):
    IDLE = "idle"
    WALK = "walk"
    JUMP = "jump"
    FALL = "fall"
    FLY = "fly"
    FLOAT = "float"
    BREATH = "breath"

# Ground tile
class GroundTile(pgt.Object):
    def __init__(self,pos,tile_id):
        self.pos = pos * cell_size
        self.tile_id = tile_id
        self.image = assets.ground_tiles[self.tile_id]
        self.rect = self.image.get_rect()
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

# Player
class Player(pgt.Object):
    def __init__(self,pos: Vector2):
        self.pos = pos * cell_size
        
        self.anim = "idle"
        self.image_index = 0
        self.image = assets.kirbo_sprite[self.anim][self.image_index]
        
        self.rect = self.image.get_rect()
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        
        self.state = PlayerState.IDLE
        
        self.can_fly = False
        
        self.vspeed = 0
        self.hspeed = 0
        self.grav = 0.2
        
        self.jump_speed = 4
        self.flap_speed = 2.5
        self.move_speed = 2
        
        self.is_on_floor = 0
        self.ground_buffer = 6
        
        self.flip_h = False
        
        self.max_fall_speed = 6
        self.max_float_speed = 2.5
        
        self.animation_timer = pgt.Timer(10, True)
    
    def switch_state(self,previous_state,state):
        self.state = state
        self.animation_timer.wait_time = 10
        
        match state:
            case PlayerState.IDLE:
                self.anim = "idle"
                self.image_index = 0
                self.animation_timer.wait_time = 15
                if previous_state == PlayerState.WALK:
                    self.animation_timer.wait_time = 10
                    self.image_index = len(assets.kirbo_sprite["idle"]) - 1
            
            case PlayerState.WALK:
                self.anim = "walk"
                self.image_index = 0
            
            case PlayerState.JUMP:
                self.anim = "jump"
                self.image_index = 0
                self.vspeed = -self.jump_speed
            
            case PlayerState.FALL:
                self.anim = "jump"
                self.animation_timer.wait_time = 3
                self.image_index = 1
            
            case PlayerState.FLY:
                self.anim = "fly"
                self.image_index = 0
                self.vspeed = -self.flap_speed
            
            case PlayerState.FLOAT:
                self.anim = "fly"
                self.image_index = 1
            
            case PlayerState.BREATH:
                self.anim = "breath"
                self.animation_timer.wait_time = 4
                self.image_index = 0
                kirbo_engine.sth.add(Smok(Vector2(self.rect.x, self.rect.y - 3), -1 if self.flip_h else 1))
                
        self.animation_timer.reset()
    
    def draw(self,surf,camera_pos):
        draw_pos_x = round(self.rect.x)
        draw_pos_y = round(self.rect.y)
        if self.anim == "fly" or self.anim == "breath":
            surf.blit(self.image,(draw_pos_x - 4 - camera_pos.x, draw_pos_y - 8 - camera_pos.y))
        else:
            surf.blit(self.image,(draw_pos_x - camera_pos.x, draw_pos_y - camera_pos.y))
    
    def update(self):
        self.dir = input.is_button_pressed(pygame.K_RIGHT) - input.is_button_pressed(pygame.K_LEFT)
        
        if pgt.place_meeting(self,self.pos.x,self.pos.y+1,kirbo_engine.ground_tiles):
            self.is_on_floor = self.ground_buffer
        if self.is_on_floor > 0: self.is_on_floor -= 1
        
        self.is_jump_button_pressed = input.is_button_just_pressed(pygame.K_z)
        self.is_jump_button_released = input.is_button_just_released(pygame.K_z)
        
        match self.state:
            case PlayerState.IDLE:
                self.vspeed += self.grav
                self.hspeed = 0
                
                if self.animation_timer.triggered():
                    if self.image_index < len(assets.kirbo_sprite[self.anim]) - 1:
                        self.image_index += 1
                
                if self.is_on_floor:
                    if self.dir != 0:
                        self.switch_state(self.state,PlayerState.WALK)
                    if self.is_jump_button_pressed:
                        self.switch_state(self.state,PlayerState.JUMP)
                else:
                    if self.vspeed > 0:
                        self.switch_state(self.state,PlayerState.FALL)
                
            case PlayerState.WALK:
                self.vspeed += self.grav
                self.hspeed = self.dir * self.move_speed
                
                if self.animation_timer.triggered():
                    self.image_index += 1
                    if self.image_index >= len(assets.kirbo_sprite[self.anim]):
                        self.image_index = 0
                
                if self.is_on_floor:
                    if self.dir == 0:
                        self.switch_state(self.state,PlayerState.IDLE)
                    if self.is_jump_button_pressed:
                        self.switch_state(self.state,PlayerState.JUMP)
                else:
                    if self.vspeed > 0:
                        self.switch_state(self.state,PlayerState.FALL)
            
            case PlayerState.JUMP:
                self.vspeed += self.grav
                self.hspeed = self.dir * self.move_speed
                
                if self.is_on_floor and self.vspeed >= 0:
                    if self.dir == 0:
                        self.switch_state(self.state,PlayerState.IDLE)
                    else:
                        self.switch_state(self.state,PlayerState.WALK)
                else:
                    if self.is_jump_button_released:
                        if self.vspeed < -2:
                            self.vspeed = -2
                    if self.vspeed > 0:
                        self.switch_state(self.state,PlayerState.FALL)
            
            case PlayerState.FALL:
                self.vspeed += self.grav*1.25
                if self.vspeed > self.max_fall_speed:
                    self.vspeed = self.max_fall_speed
                self.hspeed = self.dir * self.move_speed
                
                if self.animation_timer.triggered():
                    if self.image_index < len(assets.kirbo_sprite[self.anim]) - 1:
                        self.image_index += 1
                
                if self.is_on_floor:
                    if self.dir == 0:
                        self.switch_state(self.state,PlayerState.IDLE)
                    else:
                        self.switch_state(self.state,PlayerState.WALK)
                else:
                    if self.is_jump_button_pressed:
                        self.switch_state(self.state,PlayerState.FLY)
            
            case PlayerState.FLY:
                self.vspeed += self.grav
                self.hspeed = self.dir * self.move_speed/2
                
                if self.animation_timer.triggered():
                    if self.image_index == 0:
                        self.image_index += 1
                
                if self.is_on_floor:
                        self.switch_state(self.state,PlayerState.BREATH)
                else:
                    if self.vspeed > 0:
                        self.switch_state(self.state,PlayerState.FLOAT)
            
            case PlayerState.FLOAT:
                self.vspeed += self.grav*0.75
                if self.vspeed > self.max_float_speed:
                    self.vspeed = self.max_float_speed
                self.hspeed = self.dir * self.move_speed/2
                
                if self.is_on_floor:
                        self.switch_state(self.state,PlayerState.BREATH)
                else:
                    if self.is_jump_button_pressed:
                        self.switch_state(self.state,PlayerState.FLY)
                
            case PlayerState.BREATH:
                self.vspeed += self.grav
                self.hspeed = 0
                
                if self.animation_timer.triggered():
                    self.image_index += 1
                    if self.image_index >= len(assets.kirbo_sprite[self.anim]):
                        if self.dir == 0:
                            self.switch_state(self.state,PlayerState.IDLE)
                        else:
                            self.switch_state(self.state,PlayerState.WALK)
        
        if self.rect.y < 0:
            self.vspeed = 0
            self.rect.y = 0
        
        pgt.moving_and_collision(self,kirbo_engine.ground_tiles)
        
        if self.dir == -1: self.flip_h = True
        elif self.dir == 1: self.flip_h = False
        
        self.image = pygame.transform.flip(assets.kirbo_sprite[self.anim][self.image_index],self.flip_h,False)
        
        self.pos.x = self.rect.x
        self.pos.y = self.rect.y
        
        self.animation_timer.tick()

# Smok
class Smok(pgt.Object):
    def __init__(self,pos,dir):
        self.pos = pos
        self.dir = dir
        self.image = pygame.transform.flip(assets.kirbo_smok,self.dir == -1,False)
        self.rect = self.image.get_rect()
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        self.speed = 3
    
    def update(self):
        self.rect.x += self.dir * self.speed
        self.speed -= 0.25
        self.pos.x = self.rect.x
        if self.speed == 0:
            kirbo_engine.sth.member.remove(self)

# Game manager
class MainGame():
    def __init__(self):
        self.ground_tiles = pgt.Group()
        self.sth = pgt.Group()
        self.load_level(level)
        self.camera_pos = Vector2(0,0)
    
    def update(self):
        self.ground_tiles.draw(base_screen,self.camera_pos)
        self.player.update()
        self.player.draw(base_screen,self.camera_pos)
        self.sth.update()
        self.sth.draw(base_screen,self.camera_pos)
        
        #self.camera_pos = self.player.pos + Vector2(BASESCREEN_WIDTH/2 - 8,BASESCREEN_HEIGHT/2 - 8).multiply(-1)
        
        #self.camera_pos.x += input.is_button_pressed(pygame.K_RIGHT) - input.is_button_pressed(pygame.K_LEFT)
        #self.camera_pos.y += input.is_button_pressed(pygame.K_DOWN) - input.is_button_pressed(pygame.K_UP)
    
    def load_level(self,level):
        self.player = Player(level["player_pos"])
        levelh = len(level["map"])
        levelw = len(level["map"][0])
        for x in range(levelw):
            for y in range(levelh):
                if level["map"][y][x] != -1:
                    tile = GroundTile(Vector2(x,y),level["map"][y][x])
                    self.ground_tiles.add(tile)

# Setting up thing
time = 0
cell_size = 16
pygame.init()
base_screen = pygame.surface.Surface((BASESCREEN_WIDTH,BASESCREEN_HEIGHT))
screen = pygame.display.set_mode(Vector2(BASESCREEN_WIDTH,BASESCREEN_HEIGHT).multiply(WINDOW_SCALE).to_tuple())
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

font = pygame.font.Font(None, 16)

# Input manager
input = pgt.InputManager()

# Load images
assets = res.Assets()
assets.load()

pygame.display.set_icon(assets.kirbo_sprite["hiii"][0])

# Level tilemaps
level = {
    "player_pos" : Vector2(2,10),
    "map" : [
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1, 0, 1, 1, 1, 2,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1, 3, 4, 4, 4, 5,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1, 6, 7, 7, 7, 8,-1,-1,-1,-1,-1],
    [ 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
    [ 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5],
    ]
}

# Color
BG_COLOR = (193, 236, 228)

# game manager
kirbo_engine = MainGame()

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    input.process_events(events)
    
    base_screen.fill(BG_COLOR)
    
    kirbo_engine.update()
    
    base_screen.blit(font.render("Player state: " + str(kirbo_engine.player.state)+"\nFPS: "+ str(round(clock.get_fps())),(0,0,0),False),(0,0))
    
    screen.blit(pygame.transform.scale(base_screen, screen.get_rect().size), (0,0))
    pygame.display.flip()
    clock.tick(GAME_SPEED)