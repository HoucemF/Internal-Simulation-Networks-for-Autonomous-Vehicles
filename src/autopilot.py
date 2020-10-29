#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 10:53:17 2020

@author: houcem
"""

import carla

"""
This class defines the autopilot
affects it to the ego vehicle 
and defines its parameters
"""

class autopilot():
    
    def __init__(self, client, ego):
        
        self.client = client
        self.tm = self.client.get_trafficmanager(8000)
        self.ego = ego
        
        self.tm_port = self.tm.get_port()
        self.ego.set_autopilot(True, self.tm_port)
        
        self.tm.ignore_lights_percentage(self.ego, 100)
        