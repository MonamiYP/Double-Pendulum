import pygame
import math
import sys

(width, height) = (800, 600)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Double Pendulum Simulation - Euler")
screen.fill((0, 0, 0))

# Parameters
l1 = 150
l2 = 150
m1 = 10
m2 = 15
t1 = math.pi / 2
t2 = math.pi / 2
v1 = 0
v2 = 0
g = 1


def Euler(t1, t2, v1, v2):
    num1 = -g * (2 * m1 + m2) * math.sin(t1) - m2 * g * math.sin(t1 - 2 * t2)
    num2 = -2 * math.sin(t1 - t2) * m2 * (v2 * v2 * l2 + v1 * v1 * l1 * math.cos(t1 - t2))
    den1 = l1 * (2 * m1 + m2 - m2 * math.cos(2 * t1 - 2 * t2))
    num3 = 2 * math.sin(t1 - t2)
    num4 = v1 * v1 * l1 * (m1 + m2) + g * (m1 + m2) * math.cos(t1) + v2 * v2 * l2 * m2 * math.cos(t1 - t2)
    den2 = l2 * (2 * m1 + m2 - m2 * math.cos(2 * t1 - 2 * t2))
    a1 = (num1 + num2) / den1
    a2 = num3 * num4 / den2

    return a1, a2


def draw():
    x1 = l1 * math.sin(t1) + width / 2
    y1 = l1 * math.cos(t1) + height / 3
    x2 = x1 + l2 * math.sin(t2)
    y2 = y1 + l2 * math.cos(t2)

    # If there is a previous point (not the beginning of simulation)
    # Draw a line from the previous point to the new point of the bottom ball
    if prev_point:
        xp, yp = prev_point[0], prev_point[1]
        pygame.draw.line(trace, (100, 240, 200), (xp, yp), (x2, y2), 2)

    # Draw the trace screen (includes the line of pendulum's path) over background
    screen.blit(trace, (0, 0))

    pygame.draw.line(screen, (255, 255, 255), (width / 2, height / 3), (x1, y1), 2)
    pygame.draw.line(screen, (255, 255, 255), (x1, y1), (x2, y2), 2)
    pygame.draw.circle(screen, (70, 70, 255), (int(x1), int(y1)), m1)
    pygame.draw.circle(screen, (255, 70, 70), (int(x2), int(y2)), m2)

    return x2, y2


screen.fill((0, 0, 0))
trace = screen.copy()  # Trace to save the edited screen and blit it on new screen so line info is saved
pygame.display.update()
clock = pygame.time.Clock()
prev_point = None

while True:
    draw()
    # If window is closed, exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            sys.exit()
                    a1 = Euler(t1, t2, v1, v2)[0]
                    a2 = Euler(t1, t2, v1, v2)[1]
                    v1 += a1
                    v2 += a2
                    t1 += v1
                    t2 += v2

                    prev_point = draw()

                    pygame.display.update()