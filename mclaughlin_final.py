#!/usr/bin/env python3


##################################################
#        AstroSim 2.0 - Moss McLaughlin 6/9/16   #
#           Phys0x96 Final Project               #
#                                                #
##################################################







import pygame
from pygame.locals import *
import sys
import os
import numpy as np



##########################################

  # Settings


fps = 60                  # Frames per second
dt = 1/fps                # time rate ( real time is 1/fps)
window_size = [500,500]   # window size in pixels
center = [window_size[0]*0.5,window_size[1]*0.5]


orbital_path = True   # Shows the path of the planets
num_planets = 9
mass_sun = 1000      # to increase orbital velocity, increase G or mass_sun
G1 = 100000          # Gravitational Constant
maxmass = 2         # maximum randomly assigned mass
density = 0.01      # change size of planets [ r = (mass/density)**(1/3) ]


num_bodies = 50     
G2 = 200            # Gravitational constant
collisions = True      # set collisions on/off
panning = False      # set panning on/off
pan_speed = 1    # pan speed in pixels * fps
auto_reset = True   # Resets if all objects are off screen
reset_time = 1      # Time to check for reset (seconds)
global num_bodies =50
global G2 =200
global collide =True
global panning =False
global random_pos 




##################################################

def nbodymotion():
    pygame.display.init()
    pygame.font.init()
    pygame.display.set_caption("Astro Simulator - Moss McLaughlin - 6.2.16")
    window = pygame.display.set_mode(window_size)
    global window
    steps = 1

#################################################
    
    class body(object):
        def __init__(self,pos=None,mass=None,vel=None):
            if pos == None: self.pos =  np.random.uniform(-0.5*window_size[1],0.5*window_size[1],2)+center
            else: self.pos = pos
            if mass == None: self.mass = float(np.random.uniform(1,100,1))  
            elif mass == 'uniform': self.mass = 10
            else: self.mass = mass
            if vel== None:
                self.vel =[0,0] # np.random.uniform(-10,10,2)
            else: self.vel = vel
            self.radius = int(round((self.mass)**(1/3)))
            self.force=[0,0]
        def force(body1,body2):
            dx = body2.pos[0] - body1.pos[0]
            dy = body2.pos[1] - body1.pos[1]
            r_sq = dx*dx + dy*dy
            mag = (G2 * body1.mass * body2.mass) / r_sq
#            while mag > 100000000: mag = mag**0.5
            body1.force[0] += dx*mag/(r_sq**0.5)
            body1.force[1] += dy*mag/(r_sq**0.5)
            body2.force[0] -= dx*mag/(r_sq**0.5)
            body2.force[1] -= dy*mag/(r_sq**0.5)           
        def motion(self,dt):
            self.pos[0] += self.vel[0]*dt
            self.pos[1] += self.vel[1]*dt
            self.a = [self.force[0]/self.mass,self.force[1]/self.mass]
            self.vel[0] += dt*self.a[0]
            self.vel[1] += dt*self.a[1]
        def collision(body1,body2):
            d = body1.radius+body2.radius
            if (body2.pos[0] - body1.pos[0])*(body2.pos[0] - body1.pos[0])\
+(body2.pos[1] - body1.pos[1])*(body2.pos[1] - body1.pos[1]) < d*d: return True
#            return True

#################################################

        def draw(self,window):
            pygame.draw.circle(window,(100,150,235),\
(int(round(float(self.pos[0]))),
int(round(float(self.pos[1])))),self.radius)


##################################################

    def setup():
        global bodies
        p1 = True
        while p1 is True:
            p2 = input('\nWould you like default settings? (y/n) ')
            if p2 == 'y':
                p1 = False
                bodies = [body() for i in range(num_bodies)]
            elif p2 == 'n':
                p1 = False 

                p4 = True
                while p4 is True:
                    try: 
                        p3 = int(input('\nEnter number of bodies: '))
                        p4 = False
                        num_bodies = p3
                        global num_bodies
                    except ValueError: None

                p7 = True
                while p7 is True:
                    p8 = input('\nWould you like uniform mass? ')
                    if p8 == 'y':
                        p7 = False
                        mass = 'uniform'
                    elif p8 == 'n':
                        p7 = False
                        mass = None

                p5 = True
                while p5 is True:
                    p6 = input('\nWhat distribution would you like?\n(1) Random\n(2) Uniform\n')
                    if p6 == '1': 
                        bodies = [body(mass=mass) for i in range(num_bodies)]
                        p5 = False
                    if p6 == '2': 
                        uniform_pos = list()
                        for i in np.linspace(0,window_size[0],int((num_bodies)**0.5)):
                            for j in np.linspace(0,window_size[1],int((num_bodies)**0.5)):
                                uniform_pos.append((i,j))
                        num_bodies = len(uniform_pos)
                        global num_bodies
                        print(uniform_pos)
                        bodies = [body(mass=mass,pos = np.array(uniform_pos[i])) for i in range(num_bodies)]
                        p5 = False
        

#################################################

    def animate():
        global bodies
        window.fill((0,0,0))
        text_box.blit(text,text_pos)
        window.blit(text_box,(0,0))
        for i in bodies:
            i.draw(window)

        pygame.display.flip()

#################################################

    def move():
        for i in range(steps):
            for j in range(num_bodies):
                for k in range(j+1,num_bodies):
                    body.force(bodies[j],bodies[k])
            for j in bodies:
                j.motion(dt/steps)

    def collide():
        global bodies
        global num_bodies
        collided = []
        new = []
        for i in range(num_bodies):
            for j in range(i+1,num_bodies):
                body1 = bodies[i]
                body2 = bodies[j]
                if body.collision(body1,body2) == True:
                    collided.append(body1)
                    collided.append(body2) 
                    mass = body1.mass + body2.mass
                    pos = [0,0]
                    pos[0] = (body1.mass*body1.pos[0]+body2.mass*body2.pos[0])/mass
                    pos[1] = (body1.mass*body1.pos[1]+body2.mass*body2.pos[1])/mass
                    vel = [(body1.mass*body1.vel[0]+body2.mass*body2.vel[0])/mass,(body1.mass*body1.vel[1]+body2.mass*body2.vel[1])/mass] 
                    body3 = body(pos,mass,vel)
                    new.append(body3)
#                    print(new)
        a1 = []                      #To do the collision, erase two particles
        for i in bodies:             # from the list, add one new  
#            print(collided.count(i))    # Combine mass / momenta
            if collided.count(i) == 0:
                a1.append(i)     
        bodies = a1               
        bodies += new
        num_bodies=len(bodies)


#################################################
# Moves frame towards the most massive particle.

    def move_frame():
        mass_list = []
        for i in bodies:         
            mass_list.append(i.mass) 
        m = max(mass_list)
        biggest = [j for j, k in enumerate(mass_list) if k == m]
        if len(biggest) == 1:
            biggest = int(biggest[0])
            big_dx = bodies[biggest].pos[0]-center[0]
            big_dy = bodies[biggest].pos[1]-center[1]
            for i in bodies:
                i.pos[0] -= pan_speed*big_dx
                i.pos[1] -= pan_speed*big_dy


#################################################
# Executes all functions.

    def runit():
        global window_size
        setup()
        clock = pygame.time.Clock()
        q = 0
        text_box = pygame.Surface(window_size)
        text_box = text_box.convert()
        text_box.fill((0, 0, 0))
        font = pygame.font.Font(None,18)
        text = font.render('Press (r) to Reset, (m) for Menu, (q) to Quit.',0,(255,255,255))
        text_pos = (0.15*window_size[0],2)
        global text
        global text_box
        global text_pos
        
        k1 = True
        while k1 is True:
            for event in pygame.event.get(KEYUP):
                if event.key == K_r:
                    k1 = False
                    pygame.quit
                    runit()
                if event.key == K_q:
                    k1 = False
                    pygame.QUIT
                    os.exit()
                if event.key == K_m:
                    k1 = False
#                    pygame.QUIT
                    startup()


            move()
            if collisions is True: collide()
            if panning is True: move_frame()
            animate()
            clock.tick(fps)
            if auto_reset == True:
                q += 1
                if q == reset_time*fps:
                    q = 0
                    p = 0
                    for i in bodies:
                        if (i.pos[0]-center[0])*(i.pos[0]-center[0])+(i.pos[1]-center[1])*(i.pos[1]-center[1]) > (window_size[0])*(window_size[0]):
                            p += 1                       
                    if p == len(bodies):
                        pygame.quit()    
                        startup()
    runit()           

#################################################
# First I have to define characteristics of the orbiting bodies.


def solarsystem():
    pygame.display.init()
    pygame.font.init()
    pygame.display.set_caption("Astro Simulator - Moss McLaughlin - 6.2.16")
    window = pygame.display.set_mode(window_size)
    global window
    num_planets = 9
    fps = 60
    dt = 1/fps
    steps = 100
    center = [window_size[0]*0.5,window_size[1]*0.5]
    mass_sun = 1000  
    G = 100000       
    maxmass = 2   
    density = 0.01 

#################################################
# First I have to define characteristics of the orbiting bodies.


    class planet(object):
        def __init__(self,pos=None,mass=None):
            if pos == None:
                self.pos = np.random.uniform(-0.4*window_size[1],\
0.4*window_size[1],2) + center
            else:
                self.pos = [int(pos[0]),int(pos[1])]
            if mass == None: self.mass = float(np.random.uniform(1,maxmass,1))
            else: self.mass = mass 
            self.delta_x = self.pos[0]-center[0]
            self.delta_y = self.pos[1]-center[1]
            self.r_init =np.sqrt(self.delta_x**2 + self.delta_y**2)
            self.r = np.sqrt(self.delta_x**2 + self.delta_y**2)
            self.vel = np.sqrt(G*(self.mass+mass_sun)/self.r)
            self.radius = (self.mass/density)**(1/3)

# Here is the infinitesimal addition x2= x1+dx

        def motion(self,dt):
  
            self.delta_x = self.pos[0]-center[0]
            self.delta_y = self.pos[1]-center[1]
            self.r = np.sqrt(self.delta_x**2 + self.delta_y**2)
            self.r -= 1/self.r
            self.vel = np.sqrt(G1*(self.mass+mass_sun)/self.r)
            # note for circular orbit, dx = y * v*dt / r
            self.pos[0] -= self.delta_y*self.vel*dt/self.r
            self.pos[1] += self.delta_x*self.vel*dt/self.r

#################################################
   # Draws planets, and orbital path if true.

        def draw(self,window):
            pygame.draw.circle(window,(100,150,235),(int(round(self.pos[0])),\
int(round(self.pos[1]))),int(round(self.radius)))
            if orbital_path == True: pygame.draw.circle(window,(255,255,255),\
(int(center[0]),int(center[1])),int(self.r_init),1)

#######################################################
#     Initial conditions.
#     To reset, run setup.

    def setup():
        global planets
        l1 = True
        while l1 is True:
            l2 = input('Would you like to view our Solar System? (y/n)')
            if l2 == 'y':
                planets = our_system
                l1 = False        
            elif l2 == 'n':
                l3 = True
                l1 = False
                while l3 is True:
                    try: 
                        l4 = int(input('Enter number of planets: '))
                        num_planets = l4
                        l3 = False
                    except ValueError: None 
                     
                planets = [planet() for i in range(num_planets)]
       
#######################################################
# Draw and update picture.
# Also draws the sun.

    def animate():
        global planets
        window.fill((0,0,0))
        text_box.blit(text,text_pos)
        window.blit(text_box,(0,0))

        pygame.draw.circle(window,(255,255,0),\
(int(center[0]),int(center[1])),10)
        for i in planets:
            i.draw(window)


        pygame.display.flip()

######################################################

    def move():
        for i in range(steps):
            for j in planets:
                j.motion(dt/steps)
 
#######################################################

    def runit():
        setup()
        clock = pygame.time.Clock()
        text_box = pygame.Surface(window_size)
        text_box = text_box.convert()
        text_box.fill((0, 0, 0))
        font = pygame.font.Font(None,20)
        text = font.render('Press (r) to Reset, (m) for Menu, (q) to Quit.',0,(255,255,255))
        text_pos = (0.15*window_size[0],2)
        global text
        global text_box
        global text_pos
        k1 = True
        while k1 is True:
            for event in pygame.event.get(KEYUP):
                if event.key == K_r: 
                    k1 = False
                    pygame.quit
                    runit()                   
                if event.key == K_q:
                    k1 = False
                    pygame.QUIT
                    os.exit()
                if event.key == K_m:
                    k1 = False
#                    pygame.QUIT
                    startup()
            move()
            animate()
            clock.tick(fps)

        
######################################################

    our_system = [planet([0.05*window_size[1]+center[0],0],.1),\
    planet([0.15*window_size[1]+center[0],center[1]],1),\
    planet([0.18*window_size[1]+center[0],center[1]],2),\
    planet([0.22*window_size[1]+center[0],center[1]],1.8),\
    planet([0.26*window_size[1]+center[0],center[1]],0.8),\
    planet([0.4*window_size[1]+center[0],center[1]],12),\
    planet([0.45*window_size[1]+center[0],center[1]],8),\
    planet([0.5*window_size[1]+center[0],center[1]],.2)]    


    runit()
######################################################
#####################################################
######################################################




def startup():

    print('\n'*20)
    longstring1 = '''
 ________________________________________________________________
 
 ------- Welcome to AstroSimulator 1.0 by Moss McLaughlin ------- 
 ________________________________________________________________'''

    print(longstring1)

    longstring2 = '''
What would you like to run?
(1) for Solar System Simulator
(2) for Multi Body Motion Simulator
(3) to quit'''+'\n'*20

    choice = input(longstring2,)
    j1 = True
    while j1 == True:
        if choice == '1':
            j1 = False
            solarsystem()      
        elif choice == '2':
            j1 = False
            nbodymotion()
        elif choice == '3':     
            j1 = False
            sys.exit()
        else: 
            choice = input(longstring2)











startup()
