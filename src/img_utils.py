#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 16:54:44 2020

@author: houcem
"""

import numpy as np
import cv2
import carla

def carlaimg_to_numpy(carlaimg, segmented = False):
    if segmented == True:
        carlaimg.convert(carla.ColorConverter.CityScapesPalette)
    img = np.array(carlaimg.raw_data)
    img = img.reshape((112,112,4))
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
    return(np.copy(img))
