from math import sin, cos, sqrt, radians, acos
import pygame, os

base_path = os.path.dirname(os.path.abspath(__file__))

pygame.init()

# Object class
class Object():
    """Object class"""
    def __init__(self,pos,image):
        """Init thing"""
        self.pos = pos
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
    def draw(self,surf,camera_pos):
        """Draw thing. Support camera scrolling!"""
        draw_pos_x = round(self.rect.x)
        draw_pos_y = round(self.rect.y)
        surf.blit(self.image,(draw_pos_x - camera_pos.x, draw_pos_y - camera_pos.y))
    def spritecollide(self,group):
        """Check collision with other things"""
        for sprite in group.member:
            if self.rect.colliderect(sprite.rect):
                return True
        return False
    def update(self):
        """Code that run once per frame should be here"""
        pass

# Group class
class Group():
    def __init__(self):
        """Init thing"""
        self.member = []
    def add(self,sprite: Object):
        """Add member"""
        self.member.append(sprite)
    def draw(self,surf,camera_pos):
        """Draw things"""
        for sprite in self.member:
            sprite.draw(surf,camera_pos)
    def update(self):
        """Update things"""
        for sprite in self.member:
            sprite.update()

# Input handler
class InputManager:
    """A class to manage input"""
    def __init__(self):
        """Init thing"""
        self.pressed_buttons = []
        self.just_pressed_buttons = []
        self.just_released_buttons = []

    def process_events(self,events):
        """Update things. Should be call once per frame"""
        self.just_pressed_buttons.clear()
        self.just_released_buttons.clear()

        for event in events:
            if event.type == pygame.KEYDOWN:
                self.pressed_buttons.append(event.key)
                self.just_pressed_buttons.append(event.key)
            elif event.type == pygame.KEYUP:
                if event.key in self.pressed_buttons:
                    self.pressed_buttons.remove(event.key)
                self.just_released_buttons.append(event.key)

    def is_button_pressed(self, button):
        """Return if key is pressed"""
        return button in self.pressed_buttons

    def is_button_just_pressed(self, button):
        """Return if key is just pressed"""
        return button in self.just_pressed_buttons

    def is_button_just_released(self, button):
        """Return if key is just released"""
        return button in self.just_released_buttons
    
    def clear(self, key = -1):
        """Clear a key or all keys"""
        if key != -1:
            if key in self.pressed_buttons: self.pressed_buttons.remove(key)
            if key in self.just_pressed_buttons: self.just_pressed_buttons.remove(key)
            if key in self.just_released_buttons: self.just_released_buttons.remove(key)
        
        else:
            self.pressed_buttons.clear()
            self.just_pressed_buttons.clear()
            self.just_released_buttons.clear()

# Timer
class Timer():
    """Timer class"""
    def __init__(self,time: int,loop: bool):
        """Init thing"""
        self.wait_time = time
        self.time = self.wait_time
        self.loop = loop
        self.paused = False
    
    def tick(self):
        """tick! should be call once per frame"""
        if not self.paused and self.time >= 0: 
            self.time -= 1
        if self.loop and self.time < 0:
            self.reset()
    
    def reset(self):
        """Reset the timer"""
        self.time = self.wait_time
        
    def triggered(self):
        """Return if the timer is triggered"""
        return True if self.time == 0 else False

# UI Bar
class Bar:
    """Class for UI bar"""
    def __init__(self, x, y, width, height, color, border_width = -1, border_color = (0,0,0)):
        """Init thing"""
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.border_width = border_width
        self.border_color = border_color
        self.percent = 100
    
    def update(self, percent):
        """Update the bar"""
        self.percent = percent
    
    def draw(self, surf):
        """Draw the bar"""
        bar_rect = pygame.Rect(self.x, self.y,self.width*self.percent/100,self.height)
        border_rect = pygame.Rect(self.x - self.border_width, self.y - self.border_width,self.width + self.border_width*2,self.height + self.border_width*2)
        pygame.draw.rect(surf, self.color, bar_rect)
        pygame.draw.rect(surf, self.border_color, border_rect, self.border_width)

class Button:
    def __init__(self, x, y, image_normal, image_press, align_center = False):
        """Init thing"""
        self.can_press = True
        self.image_normal = image_normal
        self.image_press = image_press
        self.image = self.image_normal
        self.rect = self.image_normal.get_rect()
        if align_center:
            self.rect.centerx = x
            self.rect.centery = y
        else:
            self.rect.x = x
            self.rect.y = y
    def draw(self,surf):
        """Draw the button"""
        surf.blit(self.image, self.rect)
        
    def on_pressed(self):
        """Call when the button is pressed"""
        pass
    
    def on_released(self):
        """Call when the button is released"""
        pass
       
    def update(self,mouse_pos,is_mouse_button_pressed):
        """Update the button. Should be call once per frame!"""
        is_hover = point_in_rect(mouse_pos,self.rect)
        
        if is_hover and self.can_press:
            if is_mouse_button_pressed:
                self.image = self.image_press
                self.on_pressed()
                self.can_press = False
        if not is_mouse_button_pressed:
            self.can_press = True
            if self.image == self.image_press:
                self.on_released()
                self.image = self.image_normal

class TextLabel:
    """Class for text label"""
    def __init__(self,x,y,text,font,color = (0,0,0),align_center = False):
        """Init thing"""
        self.x = x
        self.y = y
        self.font = font
        self.color =color
        self.align_center = align_center
    
    def draw(self,surf):
        """Draw the label"""
        text = self.font.render(self.text,False,self.color)
        rect = text.get_rect()
        if self.align_center:
            rect.centerx = self.x
            rect.centery = self.y
        else:
            rect.x = self.x
            rect.y = self.y
        surf.blit(text,rect)

# Vector2
class Vector2():
    """Class for 2d vector"""
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def __str__(self):
        return f"({self.x},{self.y})"
    def add(self,v):
        return Vector2(self.x + v.x, self.y + v.y)
    def __add__(self,other):
        return self.add(other)
    def __sub__(self,v):
        return self.add(v.multiply(-1))
    def multiply(self,t):
        return Vector2(self.x * t, self.y * t)
    def __mul__(self,other):
        return self.multiply(other)
    def dot(self,v):
        return self.x*v.x + self.y*v.y
    def magnitude(self):
        return sqrt(self.x**2 + self.y**2)
    def normalised(self):
        length = self.magnitude()
        if length != 0:
            return Vector2(self.x/length, self.y/length)
        else:
            return Vector2(0,0)
    def angle_to(self,v):
        my_cos = (self.dot(v))/(self.magnitude()*v.magnitude())
        return acos(my_cos)
    def sign(self):
        return Vector2(sign(self.x),sign(self.y))
    def reflected(self,x,y):
        signv = Vector2(x,y).sign()
        return Vector2(self.x * signv.x, self.y * signv.y)
    def rounded(self):
        return Vector2(round(self.x), round(self.y))
    def abs(self):
        return Vector2(abs(self.x), abs(self.y))
    def is_normalised(self):
        return True if self.magnitude() == 1 else False
    def floor(self):
        return Vector2(int(self.x), int(self.y))
    def is_equal_to(self,v):
        return True if self.x == v.x and self.y == v.y else False
    def __eq__(self,other):
        return self.is_equal_to(other)
    def __ne__(self,other):
        return not self.is_equal_to(other)
    def clamped(self,limit_length):
        length = self.magnitude()
        if length <= limit_length:
            return self
        else:
            return self.normalised().multiply(limit_length)
    def to_tuple(self):
        return (self.x, self.y)
def absolute_path(relative_path):
    return os.path.join(base_path,relative_path)

def sine_wave(time, period, amplitude, midpoint):
    """Make sine wave"""
    return sin(time * 2 * 3.14159265359 / period) * amplitude + midpoint

def sine_wave_between(time, period, minimum, maximum):
    """Make sine wave between two point"""
    midpoint = minimum + (maximum-minimum)/2
    amplitude = maximum - midpoint
    return sine_wave(time, period, amplitude, midpoint)

def smooth_approach(x1,x2,spd):
    return (x2-x1)*spd

def approach(a: float,b: float,amount: float):
    """Moves "a" towards "b" by "amount" and returns the result
    Nice bcause it will not overshoot "b", and works in both directions
    Examples:
        speed = Approach(speed, max_speed, acceleration);
        hp = Approach(hp, 0, damage_amount);
        hp = Approach(hp, max_hp, heal_amount);
        x = Approach(x, target_x, move_speed);
        y = Approach(y, target_y, move_speed);
    """
    if a < b:
        a = a + amount
        if a > b:
            return b
    else:
        a = a - amount
        if a < b:
            return b
    return a

def lerp(a: float, b: float, t: float) -> float:
    """Linear interpolate on the scale given by a to b, using t as the point on that scale."""
    return (1 - t) * a + t * b

def clamp(x,min,max):
    """Clamp given number to a range"""
    if x < min: x = min
    if x > max: x = max
    return x

def sign(x):
    """Return the sign of given number"""
    if x < 0: return -1
    if x > 0: return 1
    if x == 0: return 0

def place_meeting(sprite,x,y,group):
    # Giữ vị trí hiện tại của sprite trong 2 biến startx và starty
    startx = sprite.rect.x
    starty = sprite.rect.y
    # Dịch chuyển sprite đến vị trí x,y (trong tham số)
    sprite.rect.x = x
    sprite.rect.y = y
    # Kiểm tra xem sprite có va chạm với group không, trả lại True/False tương ứng
    # Sau đó di chuyển lại sprite về vị trí ban đầu
    if sprite.spritecollide(group):
        sprite.rect.x = startx
        sprite.rect.y = starty
        return True
    sprite.rect.x = startx
    sprite.rect.y = starty
    return False    
    
def moving_and_collision(sprite, solid_group):
    ##### Di chuyển theo chiều ngang #####
    # Kiểm tra xem vị trí của sprite trong khung hình tiếp theo có chạm vào solid_group (tường, v.v) hay không.
    if place_meeting(sprite, sprite.rect.x+sprite.hspeed,sprite.rect.y,solid_group):
        # Nếu có, đẩy sprite ra khỏi tường. Cái này để tránh việc tốc độ di chuyển nhanh làm sprite bị kẹt vào tường.
        while place_meeting(sprite, sprite.rect.x + sign(sprite.hspeed),sprite.rect.y, solid_group) == False:
            sprite.rect.x += sign(sprite.hspeed)
        # Sau đó, đặt tốc độ di chuyển theo chiều ngang bằng 0 (dừng lại).
        sprite.hspeed = 0
    # Di chuyển theo chiều ngang với tốc độ là hsp
    sprite.rect.x += sprite.hspeed
    
    ##### Di chuyển theo chiều dọc #####
    # Kiểm tra xem vị trí của sprite trong khung hình tiếp theo có chạm vào solid_group (tường, v.v) hay không.
    if place_meeting(sprite, sprite.rect.x,sprite.rect.y+sprite.vspeed,solid_group):
        # Nếu có, đẩy sprite ra khỏi tường. Cái này để tránh việc tốc độ di chuyển nhanh làm sprite bị kẹt vào tường.
        while place_meeting(sprite, sprite.rect.x,sprite.rect.y + sign(sprite.vspeed), solid_group) == False:
            sprite.rect.y += sign(sprite.vspeed)
        # Sau đó, đặt tốc độ di chuyển theo chiều dọc bằng 0 (dừng lại).
        sprite.vspeed = 0
    # Di chuyển theo chiều dọc với tốc độ là vsp
    sprite.rect.y += sprite.vspeed
    