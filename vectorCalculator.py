import math
import pygame as pg


def magnitude(v):
    return math.sqrt(sum(v[i]*v[i] for i in range(len(v))))


def add(u, v):
    return [ u[i]+v[i] for i in range(len(u)) ]


def sub(u, v):
    return [ u[i]-v[i] for i in range(len(u)) ]


def dot(u, v):
    return sum(u[i]*v[i] for i in range(len(u)))


def normalize(v):
    vmag = magnitude(v)
    return [ v[i]/vmag  for i in range(len(v)) ]


def perpendicular_vector(v):
    vx = v[0]
    vy = v[1]
    if vx == 0 and vy == 0:
        raise ValueError('zero vector')

    perp_vect = pg.math.Vector2()
    perp_vect.x, perp_vect.y = -vy, vx
    return perp_vect

def rev_perpendicular_vector(v):
    vx = v[0]
    vy = v[1]
    if vx == 0 and vy == 0:
        raise ValueError('zero vector')

    rev_vect = pg.math.Vector2()
    rev_vect.x, rev_vect.y = vy, -vx
    return rev_vect

def Distance(u , v):
    return magnitude(sub(u, v))