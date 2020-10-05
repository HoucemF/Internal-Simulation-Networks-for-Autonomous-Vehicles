#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 02:14:06 2020

@author: houcem
"""

from pathlib import Path
import carla
import random
import pickle
import queue
from utils.img_utils import carlaimg_to_numpy
from PIL import Image

PATH = Path('/home/houcem/Documents/Data')

EPISODES = 50000
     
client = carla.Client('localhost', 2000)

client.set_timeout(100.0)

world = client.get_world()
settings = world.get_settings()
actor_list = []

settings.synchronous_mode = True # Disables synchronous mode
settings.fixed_delta_seconds = 0.1


blueprint_library = world.get_blueprint_library()

# Choose a vehicle blueprint at random.
vehicle_bp = blueprint_library.filter('model3')[0]
#find a camera blueprint
camera_bp = blueprint_library.find('sensor.camera.rgb')
camera_bp.set_attribute("image_size_x",str(112))
camera_bp.set_attribute("image_size_y",str(112))

spawn_points = world.get_map().get_spawn_points()

transform = spawn_points[2]
actor = world.spawn_actor(vehicle_bp, transform)
actor_list.append(actor)

camera = world.spawn_actor(camera_bp, carla.Transform(carla.Location(x=2.5, z=0.7)) , attach_to = actor)
actor_list.append(camera)
spectator = world.get_spectator()
world_snapshot = world.wait_for_tick() 
spectator.set_transform(actor.get_transform())


camera_output = queue.Queue()
control_output = queue.Queue()
world.apply_settings(settings)

file = open("results.p", "wb+")

camera.listen(lambda img : camera_output.put(carlaimg_to_numpy(img))) #Saving current input images


for i in range(EPISODES):
    
    if i % 5 == 0:
        index = i // 5 - 1
        image = None
        
        while image is None and camera_output.qsize() > 0:
            image = camera_output.get()
            Image.fromarray(image).save(PATH / 'rgb' / ('%04d.png' % index))
    
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
        
        actor.apply_control(carla.VehicleControl(throttle= car_command[0], steer= car_command[1], brake = car_command[2], reverse = car_command[3]))
        
        control_output.put(command)
        
        
    world.tick()
        
# =============================================================================
#     else:
#         if not camera_output.empty(): 
#             camera_output.get()
# =============================================================================
    
pickle.dump([list(control_output.queue)], file)    

file.close()

settings.synchronous_mode = False # Enables synchronous mode
world.apply_settings(settings)

for a in actor_list:
    a.destroy()