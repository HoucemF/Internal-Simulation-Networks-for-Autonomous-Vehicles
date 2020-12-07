#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 22:10:14 2020

@author: houcem
"""


from sim_env import Sim_env
from time import sleep
import carla

env = Sim_env(town = "Town03")
print(len(env.world.get_map().get_spawn_points()))
env.clean_up()
