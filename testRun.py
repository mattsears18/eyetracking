#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 19:38:21 2017

@author: mattsears
"""

from eyetracking import *

files = ['./BeGaze Data/Raw Data/Participant 01.txt',]
aois = ['Spool 1']
periods = [3000]

makeConvexHullAnimations(files, periods, aois)








# AFTER TESTING

files = [
    './BeGaze Data/Raw Data/Participant 01.txt',
    './BeGaze Data/Raw Data/Participant 02.txt',
    './BeGaze Data/Raw Data/Participant 03.txt',
    './BeGaze Data/Raw Data/Participant 04.txt',
    './BeGaze Data/Raw Data/Participant 05.txt',
    './BeGaze Data/Raw Data/Participant 06.txt',
    './BeGaze Data/Raw Data/Participant 07.txt',
    './BeGaze Data/Raw Data/Participant 08.txt',
    './BeGaze Data/Raw Data/Participant 09.txt',
    './BeGaze Data/Raw Data/Participant 10.txt',
    './BeGaze Data/Raw Data/Participant 11.txt',
    './BeGaze Data/Raw Data/Participant 12.txt',
    './BeGaze Data/Raw Data/Participant 13.txt',
    './BeGaze Data/Raw Data/Participant 14.txt',
    './BeGaze Data/Raw Data/Participant 15.txt',
    './BeGaze Data/Raw Data/Participant 16.txt',
    './BeGaze Data/Raw Data/Participant 17.txt',
    './BeGaze Data/Raw Data/Participant 18.txt',
    './BeGaze Data/Raw Data/Participant 19.txt',
    './BeGaze Data/Raw Data/Participant 20.txt',
]

aois = [
    'Spool 1',
    'Spool 2',
    'Spool 3',
    'Spool 4',
    'Spool 5',
    'Spool 6',
    'Spool 7',
    'Spool 8',
    'Spool 9',
    'Spool 10',
]

periods = [
    3000,
    4000,
    5000,
    6000,
    7000,
    8000,
    9000,
    10000,
    12000,
    15000
]
