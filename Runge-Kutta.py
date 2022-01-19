import pygame
import sys
from math import sin, cos, pi
import numpy as np
from numpy.linalg import inv

pygame.display.set_caption("Double Pendulum Simulation - RK4")

# Parameters and variables
width, height = 700, 480
offset = (350, 100)

m1, m2 = 1.5, 1
l1, l2 = 1.5, 1.5
a1, a2 = pi / 4, -1
g = 9.81


# Function that gets input data of y and calculates acceleration
def acceleration(y):
    a1d, a2d = y[0], y[1]
    a1, a2 = y[2], y[3]

    m11, m12 = (m1 + m2) * l1, m2 * l2 * cos(a1 - a2)
    m21, m22 = l1 * cos(a1 - a2), l2
    m = np.array([[m11, m12], [m21, m22]])

    f1 = -m2 * l2 * a2d * a2d * sin(a1 - a2) - (m1 + m2) * g * sin(a1)
    f2 = l1 * a1d * a1d * sin(a1 - a2) - g * sin(a2)
    f = np.array([f1, f2])

    accel = inv(m).dot(f)  # Matrix multiplication to find a, F = ma

    return np.array([accel[0], accel[1], a1d, a2d])


# Runge-Kutta 4th Order method to find next value of y for a given t using step size dt
def RK4_step(y, t, dt):
    k1 = acceleration(y)
    k2 = acceleration(y + 0.5 * dt * k1)
    k3 = acceleration(y + 0.5 * dt * k2)
    k4 = acceleration(y + dt * k3)

    return dt * (k1 + k2 * 2 + k3 * 2 + k4) / 6


# Find the coordinates of the position of bobs
def coordinates(theta1, theta2):
    scale = 100
    # (x1, y1) coordinates of first pendulum
    x1 = l1 * scale * sin(theta1) + offset[0]
    y1 = l1 * scale * cos(theta1) + offset[1]
    # (x2, y2) coordinates of second pendulum
    x2 = x1 + l2 * scale * sin(theta2)
    y2 = y1 + l2 * scale * cos(theta2)

    return (x1, y1), (x2, y2)


# Function to draw stuff on screen
def draw(point1, point2):
    scale = 5

    # Set coordinates of the balls
    x1, y1 = int(point1[0]), int(point1[1])
    x2, y2 = int(point2[0]), int(point2[1])

    # If there is a previous point (not the beginning of simulation)
    # Draw a line from the previous point to the new point of the bottom ball
    if prev_point:
        xp, yp = prev_point[0], prev_point[1]
        pygame.draw.line(trace, (200, 100, 255), (xp, yp), (x2, y2), 2)

    # Draw the trace screen (includes the line of pendulum's path) over background
    screen.blit(trace, (0, 0))

    pygame.draw.line(screen, (255, 255, 255), offset, (x1, y1), 5)
    pygame.draw.line(screen, (255, 255, 255), (x1, y1), (x2, y2), 5)
    pygame.draw.circle(screen, (255, 255, 255), offset, 8)
    pygame.draw.circle(screen, (255, 0, 0), (x1, y1), int(m1 * scale))
    pygame.draw.circle(screen, (0, 0, 255), (x2, y2), int(m2 * scale))

    return x2, y2


# Initializing the displays
screen = pygame.display.set_mode((width, height))
screen.fill((0, 0, 0))
trace = screen.copy()  # Trace to save the edited screen and blit it on new screen so line info is saved
pygame.display.update()
clock = pygame.time.Clock()

prev_point = None
t = 0.0
dt = 0.02
y = np.array([0.0, 0.0, pi / 2, pi / 2])  # Initial values of thetas

while True:
    # If window is closed, exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # Find the coordinates of points given the angles
    point1, point2 = coordinates(y[2], y[3])
    # Display the stuff on screen by calling draw function
    # Then return coordinates of end of pendulum
    # Prev_point is the previous point of the ball so that the path can be drawn
    prev_point = draw(point1, point2)

    # Increase time, find appropriate coordinates for new point in time
    t += dt
    y = y + RK4_step(y, t, dt)

    clock.tick(60)
    pygame.display.update()
