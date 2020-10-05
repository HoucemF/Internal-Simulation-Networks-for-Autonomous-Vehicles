#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 00:38:29 2020

@author: houcem
"""

import random 

"""
This method returns a random command for the agent
in the form of a list
"""

def babbling():
    command =  []
    
    dice_roll = random.uniform(0, 1)
    if dice_roll < 0.33:
        command = [random.uniform(0,1), random.uniform(-1,1), 0, 0] # The car moves forward
    else: 
        if dice_roll < 0.66 and dice_roll > 0.33:
            command = [random.uniform(0,1), random.uniform(-1,1), 0, 1] # The car moves backwards
        else: command = [0, random.uniform(-1,1), random.uniform(0, 1), 0] # The car uses the break
    
    car_command = command.copy()
        
    if command[3] == 0: 
        car_command[3] = False 
    else: car_command[3] = True
    
    return [command, car_command]