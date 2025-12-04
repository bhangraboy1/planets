# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import pygame
import math

pygame.init()
WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARKGREY = (80, 78, 81)

FONT = pygame.font.SysFont("comicsans", 16)
class Planet:
# Astronomical Units
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 250 / AU
    TIMESTEP = 60*60*24 / 2 # 1 day
    #mass in kgs
    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.distancetosun = 0

        self.xvel = 0
        self.yvel = 0

    def draw (self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x,y))
            pygame.draw.lines(win, self.color, False, updated_points, 2)

        pygame.draw.circle(win, self.color, (x,y), self.radius)
        if not self.sun:
            distance_text = FONT.render(f"{round(self.distancetosun/1000,1)}km", 1, WHITE)
            win.blit(distance_text, (x- distance_text.get_width()/2 ,y- distance_text.get_height()/2  ) )

    def writetime(self, win, count):
        time_text = FONT.render(f"{round(count, 1)}weeks", 1, WHITE)
        win.blit(time_text, (10, 10))


    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)
        if other.sun:
            self.distancetosun = distance
        force = (self.G * self.mass * other.mass) / (distance ** 2)
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy
        self.xvel += total_fx / self.mass * self.TIMESTEP
        self.yvel += total_fy / self.mass * self.TIMESTEP

        # F = ma
        # a = F/m
        # Del V = a * Del T

        self.x += self.xvel * self.TIMESTEP
        self.y += self.yvel * self.TIMESTEP
        self.orbit.append((self.x, self.y))

def simulation():
    # Use a breakpoint in the code line below to debug your script.
    print('Hi')  # Press ⌘F8 to toggle the breakpoint.
    run = True
    clock = pygame.time.Clock()
    sun = Planet(0, 0, 30, YELLOW, 1.9982 * 10**30)
    sun.sun = True

    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.972 * 10**24)
    earth.yvel = 29.783 * 1000

    moon = Planet(-1.02 * Planet.AU, 0, 5, WHITE, 7.346 * 10**22)
    moon.yvel = 29.783 * 1000
    moon.xvel = 0 * 1000

    mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39 * 10**23)
    mars.yvel = 24.077 * 1000

    mercury = Planet(+0.387*Planet.AU, 0, 8, DARKGREY, 3.30 * 10**23)
    mercury.yvel = -47.4 * 1000

    venus = Planet(+0.723*Planet.AU, 0, 14, WHITE, 4.8605 * 10**24)
    venus.yvel = -35.02 * 1000

    asteroid1 = Planet(2 * Planet.AU, Planet.AU, 2, BLUE, 2 * 10**22)
    asteroid1.yvel = 0 * 1000
    asteroid2 = Planet(Planet.AU+1, Planet.AU+1, 2, WHITE, 2 * 10**22)
    asteroid2.yvel = 1 * 1000
    asteroid3 = Planet(1.5 * Planet.AU, Planet.AU, 2, RED, 2 * 10**22)
    asteroid3.yvel = 3.9 * 1000
    planets = [sun, earth, mars, mercury, venus, asteroid1, asteroid2, asteroid3]
    count = 0

    while run:
        clock.tick()
        WIN.fill((0,0,0))
#        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)
        count += 1
        if ((count % 14) == 0): planet.writetime(WIN, count/14)
        pygame.display.update()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    simulation()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
