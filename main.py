# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import math
from typing import Tuple, Union, List
import logging
import pygame

logging.basicConfig(level=logging.DEBUG)
SPEED_INCR = 0.10
MOUSE_BOUNCE_FACTOR = 1.25


def round_to_speed_incr(obj: Union[float, Tuple[float, float], List[float]]) -> Union[float, Tuple[float, float], List[float]]:
    if type(obj) is tuple:
        return round_to_speed_incr(obj[0]), round_to_speed_incr(obj[1])
    if type(obj) is list:
        obj[0] = round_to_speed_incr(obj[0])
        obj[1] = round_to_speed_incr(obj[1])
        return obj
    div = int(obj / SPEED_INCR)
    retval = float(div) * SPEED_INCR
    return retval



def pythagorean(a: float, b: float) -> float:
    return math.sqrt(math.pow(a, 2) + math.pow(b, 2))


def bounce_vector(radius: int, ball_center: Tuple[int, int], current_vector: Tuple[float, float],
                  mouse_click: Tuple[int, int]) -> Tuple[float, float]:
    """
    Given a mouse click on a ball, calculate the vector to be added to the ball's speed.
    :param radius: Radius of the ball in px
    :param ball_center: Current position of the ball on the screen
    :param current_vector: Current vector of the ball's motion
    :param mouse_click: Point at which the mouse was clicked
    :return: tuple(x, y): New vector to be added to the ball's direction
    """
    current_speed = pythagorean(*current_vector)
    logging.debug(f'bounce_vector: current_speed = {current_speed}')
    click_offset = (float(mouse_click[0]) - ball_center[0], float(mouse_click[1]) - ball_center[1])
    logging.debug(f'bounce_vector: click_offset = {click_offset}')
    click_dist_from_center = pythagorean(*click_offset)
    logging.debug(f'bounce_vector: click_dist_from_center = {click_dist_from_center}')
    force_magnitude = max(math.sin(click_dist_from_center / float(radius) * math.pi) * MOUSE_BOUNCE_FACTOR, 0)
    logging.debug(f'bounce_vector: force_magnitude = {force_magnitude}')
    speed_of_add_vector = force_magnitude
    logging.debug(f'bounce_vector: speed_of_add_vector = {speed_of_add_vector}')
    angle = abs(math.atan(click_offset[1] / click_offset[0] if click_offset[0] != 0 else 1))
    logging.debug(f'bounce_vector: angle = {angle}')
    abs_x = math.cos(angle) * speed_of_add_vector
    abs_y = math.sin(angle) * speed_of_add_vector
    logging.debug(f'bounce_vector: abs = {(abs_x, abs_y)}')
    add_v_x = math.copysign(abs_x, -click_offset[0])
    add_v_y = math.copysign(abs_y, -click_offset[1])
    logging.debug(f'bounce_vector: add_v = {(add_v_x, add_v_y)}')
    return round_to_speed_incr((add_v_x, add_v_y))


def main():
    TARGET_FPS = 60
    pygame.init()

    size = width, height = 1024, 768
    speed = [2.0, 2.0]
    pos = [0.0, 0.0]
    black = 0, 0, 0

    screen = pygame.display.set_mode(size)
    ball = pygame.image.load('intro_ball.gif')
    pygame.display.set_caption('Bouncing Ball')
    ballrect = ball.get_rect()

    clock = pygame.time.Clock()

    while True:
        modpress = pygame.key.get_mods()
        if modpress & pygame.KMOD_LSHIFT:
            magnitude = 1.0
        else:
            magnitude = SPEED_INCR
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                logging.debug('mouseclick')
                if ballrect.collidepoint(pygame.mouse.get_pos()):
                    b_w, b_h = ballrect.size
                    radius = b_w // 2
                    ball_center = ballrect.center
                    mouse_click = pygame.mouse.get_pos()
                    speed_t = tuple(speed)
                    new_v = bounce_vector(radius, ball_center, speed_t, mouse_click)
                    logging.debug(f'bounce_vector({radius}, {ball_center}, {speed_t}, {mouse_click}) -> {new_v}')
                    speed[0] += new_v[0]
                    speed[1] += new_v[1]
            if event.type == pygame.KEYDOWN:
                logging.debug('keydown')
                if event.key == pygame.K_w:
                    speed[1] -= magnitude
                elif event.key == pygame.K_s:
                    speed[1] += magnitude
                elif event.key == pygame.K_a:
                    speed[0] -= magnitude
                elif event.key == pygame.K_d:
                    speed[0] += magnitude
                elif event.key == pygame.K_q:
                    return

        speed = round_to_speed_incr(speed)
        pos[0] += speed[0]
        pos[1] += speed[1]
        ballrect.x = int(pos[0])
        ballrect.y = int(pos[1])
        if ballrect.left <= 0 or ballrect.right >= width:
            speed[0] = -speed[0]
        if ballrect.top <= 0 or ballrect.bottom >= height:
            speed[1] = -speed[1]

        screen.fill(black)
        screen.blit(ball, ballrect)
        pygame.display.flip()
        pygame.time.Clock()
        clock.tick(TARGET_FPS)


if __name__ == '__main__':
    main()
