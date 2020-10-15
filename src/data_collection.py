#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 22:55:53 2020

@author: houcem
"""

from sim_env import Sim_env
from camera import Camera
from control import babbling
import pickle
import sys
import getopt
import carla
from pathlib import Path
from PIL import Image

"""
This script will mine the sensor output
from the simulation
It requires carla to be open and connected to port 2000
Running the script takes arguments: 
        -p to specify the path
        -e to specify the number of episodes
        -f to specify the number of frames skipped
"""

def main(argv):
    
    episodes = 150000
    frame_skip = 5
    home_path = Path.home()
    save_path = (home_path / 'data')
    
    #Reading arguments
    try:
        opts, args = getopt.getopt(argv, "he:f:p:")
    except getopt.GetoptError:
        print("data_collection -p <Save path> -e <number of episodes> -f <number of frames skipped>")       
        sys.exit(2)
        
    for opt, arg in opts:
        if opt == '-h':
             print ("data_collection -p <Save path> -e <number of episodes> -f <number of frames skipped>")    
             sys.exit()
        elif opt == "-p":
             save_path = Path(arg)
        elif opt == "-e":
             episodes = int(arg)
        elif opt == "-f":
             frame_skip = int(arg)
    
    
    #Defining the environement and getting the actors
    env = Sim_env()
    env.spawn_ego()
    camera = Camera(env.world, env.blueprints, env.ego)
    
    #spawning a spectator to watch the car from above
    spectator = env.world.get_spectator()
    spectator.set_transform( carla.Transform(
                env.ego.get_location() + carla.Location(z=50),
                carla.Rotation(pitch=-90)))
    
    #creating a save location and the save files
    save_path.mkdir(parents=True, exist_ok=True)
    motor_output_file = open(save_path / "motor_output.p", "wb+")
    Path(save_path / "rgb").mkdir(parents=True, exist_ok=True)
    motor_output = []
    
    #Taking control of the simulation
    env.enter()
    
    #Simulating
    for i in range(episodes):
        
        #Every cycle of frames apply motor control and get sensor output
        if i % frame_skip == 0:
            
            index = i // frame_skip - 1
            image = None
            
            while image is None and camera.queue.qsize() > 0:
                image = camera.get()
                Image.fromarray(image).save(save_path / 'rgb' / ('%04d.png' % index))
                
            ego_command = babbling()
            car_command = ego_command[1]
            command = ego_command[0]
            
            env.ego.apply_control(carla.VehicleControl(throttle= car_command[0], steer= car_command[1], brake = car_command[2], reverse = car_command[3]))
            
            motor_output.append(command)
        
        env.world.tick()
        
    #saving the motor output to file
    pickle.dump(list(motor_output), motor_output_file)    
    
    #cleaning_up
    motor_output_file.close()
    env.clean_up()

if __name__ == "__main__":
    main(sys.argv[1:])