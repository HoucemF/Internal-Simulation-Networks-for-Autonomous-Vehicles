#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 01:14:42 2020

@author: houcem
"""

import carla


def set_sync_mode(client, sync):
    world = client.get_world()

    settings = world.get_settings()
    settings.synchronous_mode = sync
    settings.fixed_delta_seconds = 1.0 / 10.0

    world.apply_settings(settings)

"""
This class instantiates the environnement of the selection
It creates the actors and is used to run the simulation

"""

class Sim_env:
    
    
    """
    The constructor for the environnement
    It enables the selection of the town and the weather
    of where the simulation is happening. Also, the port
    on which the client will connect.    
    """
    def __init__(self, port = 2000, town = 'Town03'):
        self.client = carla.Client('localhost', port)
        self.client.set_timeout(100.0)
        
        
        #Selecting the town and loading its map
        self.town = town
        self.world = self.client.load_world(town)
        
        #Getting a list of the blueprints
        self.blueprints = self.world.get_blueprint_library()
        
        #Creating the ego vehicle's space we will create it later
        self.ego = None
        
        #A list that tracks all the actors 
        self.actor_list = []
        
        #Another list to track the sensors
        self.sensor_list = []
        
    """
    The method spawns a vehicle that is the ego vehicle 
    of the simulation
    """        
    def spawn_ego(self, spawn_point = 2):
        vehicle_bp = self.blueprints.filter('model3')[0]
        self.ego = self.world.spawn_actor(vehicle_bp, self.world.get_map().get_spawn_points()[spawn_point])
        self.actor_list.append(self.ego)
            
    """
    This method syncs the simulation and the client
    """        
      
    def enter(self):
        set_sync_mode(self.client, True)
        
    """
    This method applies cleans up the simulation and 
    returns it to asynchoronous mode
    """
    
    def clean_up(self):
        set_sync_mode(self.client, False)
        for actor in self.actor_list:
            actor.destroy()
