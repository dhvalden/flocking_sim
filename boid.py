import random
import math
import pygame
import miscFunctions
from miscFunctions import rotatePolygon, constrainMin, mapVal

def init(width, height, surface):
    global the_width, the_height, the_surface
    the_width = width
    the_height = height
    the_surface = surface

class Boid(object):
    def __init__(self, x, y):
        self.pos = pygame.math.Vector2(x, y)
        self.vel = pygame.math.Vector2(random.randint(-1, 1), random.randint(-1, 1))
        self.acc = pygame.math.Vector2(0, 0)
        self.vertices = self.createVertices()
        self.maxspeed = 5
        self.maxforce = 0.07

    def createVertices(self):
        a = (self.pos[0], self.pos[1] - 9)
        b = (self.pos[0] - 3, self.pos[1] + 3)
        c = (self.pos[0] + 3, self.pos[1] + 3)
        return [a, b, c]

    def arrive(self, target):
        desired = target - self.pos
        dist = desired.length()
        speed = self.maxspeed
        if dist < 100:
            speed = mapVal(dist, 0, 100, 0, self.maxspeed)
        try:
            desired.scale_to_length(speed)
        except ValueError:
            pass
        steer = desired - self.vel
        if steer.length() > self.maxforce:
            steer.scale_to_length(self.maxforce)
        return steer

    def seek(self, target):
        desired = target - self.pos
        desired.scale_to_length(self.maxspeed)
        steer = desired - self.vel
        if steer.length() > self.maxforce:
            steer.scale_to_length(self.maxforce)
        return steer

    def applyForce(self, force):
        self.acc += force

    def update(self):
        self.vel += self.acc
        self.pos += self.vel
        self.acc *= 0
        self.vertices = self.createVertices()

    def show(self):
        angle = math.degrees(math.atan2((self.pos[1] + self.vel[1]) - self.pos[1],
                (self.pos[0] + self.vel[0]) - self.pos[0])) + 90
        vert = rotatePolygon(self.vertices, angle, (self.pos[0], self.pos[1]))
        pygame.draw.polygon(the_surface, (255, 255, 255), vert, 1)

    def borders(self):
        if self.pos[0] < 0: self.pos[0] = the_width
        if self.pos[1] < 0: self.pos[1] = the_height
        if self.pos[0] > the_width: self.pos[0] = 0
        if self.pos[1] > the_height: self.pos[1] = 0

    def separate(self, boids):
        desiredsep = 20
        steer = pygame.math.Vector2(0, 0)
        count = 0
        for boid in boids:
            dist = self.pos.distance_to(boid.pos)
            if dist > 0 and dist < desiredsep:
                diff = self.pos - boid.pos
                diff.normalize()
                diff /= dist
                steer += diff
                count += 1
        if count > 0:
            steer /= count
        if steer.length() > 0:
            steer.normalize()
            steer *= self.maxspeed
            steer -= self.vel
            if steer.length() > self.maxforce:
                steer.scale_to_length(self.maxforce)
        return steer

    def align (self, boids):
        neighbordist = 60
        add = pygame.math.Vector2(0, 0)
        count = 0
        for boid in boids:
            dist = self.pos.distance_to(boid.pos)
            if dist > 0 and dist < neighbordist:
                add += boid.pos
                count += 1
        if count > 0:
            add /= count
            try:
                add.normalize()
            except ValueError:
                pass
            add *= self.maxspeed
            steer = add - self.vel
            if steer.length() > self.maxforce:
                steer.scale_to_length(self.maxforce)
            return steer
        else:
            return pygame.math.Vector2(0, 0)

    def cohesion (self, boids):
        neighbordist = 60
        add = pygame.math.Vector2(0, 0)
        count = 0
        for boid in boids:
            dist = self.pos.distance_to(boid.pos)
            if dist > 0 and dist < neighbordist:
                add += boid.pos
                count += 1
        if count > 0:
            add /= count
            return self.seek(add)
        else:
            return pygame.math.Vector2(0, 0)

    def flock(self, boids):
        sep = self.separate(boids)
        ali = self.align(boids)
        coh = self.cohesion(boids)
        sep *= 3
        ali *= 1.2
        coh *= 1.3
        self.applyForce(sep)
        self.applyForce(ali)
        self.applyForce(coh)

    def run(self, boids):
        self.flock(boids)
        self.update()
        self.borders()
        self.show()
