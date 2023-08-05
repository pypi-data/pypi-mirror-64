#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, print_function, absolute_import,
                        unicode_literals)

# ALMA processing parameters
pbband = {
    'b3' : 80.,
    'b4' : 50.,
    'b5' : 40.,
    'b6' : 29.,
    'b7' : 22.,
    'b8' : 16.,
    'b9' : 10.,
    'b10' : 8.
}

# constants
arcsec = 4.84813681109536e-06   # radians
clight = 2.99792458e+8          # [m/s] Speed of light

# utility functions
def get_goodpix(a):
    if (a % 2) != 0: a += 1
    work = True
    while work:
        aa = a
        due = True
        tre = False
        cinque = False
        sette = False
        while due:
            b = aa / 2
            if b == 1:
                work = False
            aa = b
            if (aa % 2) != 0:
                due = False
        if (aa % 3) == 0:
            tre = True
        while tre:
            b = aa / 3
            if b == 1:
                work = False
            aa = b
            if (aa % 3) != 0:
                tre = False
        if (aa % 5) == 0:
            cinque = True
        while cinque:
            b = aa / 5
            if b == 1:
                work = False
            aa = b
            if (aa % 5) != 0:
                cinque = False
        if (aa % 7) == 0:
            sette = True
        while sette:
            b = aa / 7
            if b == 1:
                work = False
            aa = b
            if (aa % 7) == 0:
                sette = False
        if work:
            a += 2
    return a