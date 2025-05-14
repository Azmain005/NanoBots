from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random
import time
import platform

if platform.system() == 'Darwin':
    import os
    os.environ['PYOPENGL_PLATFORM'] = 'darwin'

# Game state variables
game_state = "PLAYING"
player_health = 100
score = 0
level = 1
level_duration = 60
level_start_time = time.time()
game_start_time = time.time()
cheat_mode = False
boss_active = False
boss_spawned_this_level = False
final_play_time = 0
base_player_speed = 0.1
speed_increase_rate = 0.00005
base_virus_spawn_rate = 0.001
game_paused = False
game_speed_factor = 0.75
game_speed_increase_rate = 0.0001
max_game_speed = 1.5

# Camera and movement variables
player_pos = [0, 0, -100]
player_velocity = [0, 0, -0.5]
camera_offset = [0, 20, 30]
camera_pos = [player_pos[0] + camera_offset[0],
              player_pos[1] + camera_offset[1],
              player_pos[2] + camera_offset[2]]

move_left = False
move_right = False
move_up = False
move_down = False
move_speed = 0.25
max_lateral_pos = 40
max_vertical_pos = 40

fovY = 70
last_time = 0
GRID_LENGTH = 600

# Game environment parameters
TUNNEL_RADIUS = 50
TUNNEL_SEGMENT_LENGTH = 100
TUNNEL_SEGMENTS = 35
PULSE_AMPLITUDE = 3
PULSE_SPEED = 0.0015

# Game objects
viruses = []
bullets = []
shoot_cooldown = 0
boss_bullets = []
boss_shoot_timer = 0

powerups = []
active_powerups = {
    "speed": {"active": False, "end_time": 0},
    "magnet": {"active": False, "end_time": 0},
    "laser": {"active": False, "end_time": 0},
    "invincibility": {"active": False, "end_time": 0}
}
oxygen_collectibles = []
virus_kill_tint_timer = 0

fpp_view = False

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_health_bar():
    bar_width = 200
    bar_height = 20
    x = 10
    y = 770
    
    glColor3f(0.7, 0.7, 0.7)
    glBegin(GL_QUADS)
    glVertex2f(x-2, y-2)
    glVertex2f(x+bar_width+2, y-2)
    glVertex2f(x+bar_width+2, y+bar_height+2)
    glVertex2f(x-2, y+bar_height+2)
    glEnd()
    
    health_percentage = max(0, player_health) / 100.0
    health_width = bar_width * health_percentage
    
    if player_health > 60:
        glColor3f(0, 1, 0)
    elif player_health > 30:
        glColor3f(1, 1, 0)
    else:
        glColor3f(1, 0, 0)
    
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x+health_width, y)
    glVertex2f(x+health_width, y+bar_height)
    glVertex2f(x, y+bar_height)
    glEnd()
    
    glColor3f(1, 1, 1)
    draw_text(x+5, y+5, f"Health: {player_health}%")

def draw_hud():
    draw_health_bar()
    draw_text(800, 770, f"Score: {score}")
    draw_text(10, 730, f"Level: {level}")
    
    panel_x = 10
    panel_y = 600
    line_height = 25
    preview_offset_x = 10
    preview_offset_y = 8
    preview_size = 18
    text_offset_x = 40
    
    glColor4f(0.0, 0.0, 0.0, 0.7)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glBegin(GL_QUADS)
    glVertex2f(panel_x - 5, panel_y - 5)
    glVertex2f(panel_x + 300, panel_y - 5)
    glVertex2f(panel_x + 300, panel_y + 200)
    glVertex2f(panel_x - 5, panel_y + 200)
    glEnd()
    glDisable(GL_BLEND)
    
    glColor3f(1.0, 1.0, 1.0)
    draw_text(panel_x, panel_y, "Collectible Items", GLUT_BITMAP_HELVETICA_18)
    
    def draw_item_preview_2d(x, y, item_type):
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, 1000, 0, 800)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        glTranslatef(x, y, 0)
        glScalef(preview_size, preview_size, 1)
        if item_type == "speed":
            glColor3f(0.0, 0.6, 1.0)
            glutSolidCube(0.5)
            glColor3f(1.0, 1.0, 1.0)
            sphere = gluNewQuadric()
            gluSphere(sphere, 0.18, 12, 12)
            gluDeleteQuadric(sphere)
        elif item_type == "magnet":
            glColor3f(0.8, 0.2, 1.0)
            glutSolidCube(0.5)
            glColor3f(1.0, 1.0, 1.0)
            sphere = gluNewQuadric()
            gluSphere(sphere, 0.18, 12, 12)
            gluDeleteQuadric(sphere)
        elif item_type == "laser":
            glColor3f(1.0, 0.2, 0.2)
            glutSolidCube(0.5)
            glColor3f(1.0, 1.0, 1.0)
            sphere = gluNewQuadric()
            gluSphere(sphere, 0.18, 12, 12)
            gluDeleteQuadric(sphere)
        elif item_type == "health":
            glColor3f(0.2, 1.0, 0.2)
            glutSolidCube(0.5)
            glColor3f(1.0, 1.0, 1.0)
            sphere = gluNewQuadric()
            gluSphere(sphere, 0.18, 12, 12)
            gluDeleteQuadric(sphere)
        elif item_type == "invincibility":
            glColor3f(1.0, 0.2, 0.8)
            glutSolidCube(0.5)
            glColor3f(1.0, 1.0, 1.0)
            sphere = gluNewQuadric()
            gluSphere(sphere, 0.18, 12, 12)
            gluDeleteQuadric(sphere)
        elif item_type == "oxygen":
            glColor3f(1.0, 1.0, 1.0)
            sphere = gluNewQuadric()
            gluSphere(sphere, 0.25, 8, 8)
            gluDeleteQuadric(sphere)
            glColor3f(1.0, 1.0, 1.0)
            glPointSize(3.0)
            glBegin(GL_POINTS)
            glVertex3f(0, 0, 0)
            glEnd()
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW) 