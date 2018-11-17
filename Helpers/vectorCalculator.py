import math
import pygame as pg


def magnitude(v):
    return math.sqrt(sum(v[i]*v[i] for i in range(len(v))))


def add(u, v):
    return [u[i]+v[i] for i in range(len(u))]


def sub(u, v):
    return [u[i]-v[i] for i in range(len(u))]


def dot(u, v):
    return sum(u[i]*v[i] for i in range(len(u)))


def normalize(v):
    vmag = magnitude(v)
    return [v[i]/vmag for i in range(len(v))]


def perpendicular_vector(v):
    if v.x == 0 and v.y == 0:
        raise ValueError('zero vector')

    perp_vect = pg.math.Vector2()
    perp_vect.x, perp_vect.y = -v.y, v.x
    return perp_vect


def distance(u, v):
    return magnitude(sub(u, v))

