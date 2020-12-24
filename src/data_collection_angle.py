#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 20:32:05 2020

@author: houcem
"""
import pickle
import sys
import getopt
from pathlib import Path
from PIL import Image

import carla

from sim_env import Sim_env
from camera import Camera
from control import babbling_angle
from datetime import datetime


def main(argv):
 
    """
    This script will mine the sensor output
    from the simulation
    It requires carla to be open and connected to port 2000
    Running the script takes arguments:
            -p to specify the path
            -e to specify the number of episodes
            -f to specify the number of frames skipped
    """


    frame_skip = 5
    home_path = Path.home()
    save_path = (home_path / 'data_babbling_5')
    segmentation = False

    #Reading arguments
    try:
        opts, args = getopt.getopt(argv, "he:f:p:")
    except getopt.GetoptError:
        print("data_collection_angle -p <Save path>")
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print ("data_collection_angle -p <Save path>")
            sys.exit()
        elif opt == "-p":
            save_path = Path(arg)
        


    #Defining the environement 
    env = Sim_env()

    #creating a save location and the save files
    save_path.mkdir(parents=True, exist_ok=True)
    motor_output_file = open(save_path / "motor_output.p", "wb+")
    Path(save_path / "rgb").mkdir(parents=True, exist_ok=True)
    motor_output = []

    i = 0
    env.spawn_ego(spawn_point=0)
    camera = Camera(env.world, env.blueprints, env.ego, segmentation)

    #spawning a spectator to watch the car from above
    spectator = env.world.get_spectator()
    env.enter()

    
    for spawn_pt in env.world.get_map().get_spawn_points():
                
        env.ego.set_transform(spawn_pt)
        for j in range(250):            
            env.world.tick()
            spectator.set_transform( carla.Transform(
                    env.ego.get_location() + carla.Location(z=50),
                    carla.Rotation(pitch=-90)))
            
            if j % frame_skip == 0:
                
                index = j // frame_skip
                image = None
                
                while image is None and camera.queue.qsize() > 0:
                    image = camera.get()
                    Image.fromarray(image).save(save_path / 'rgb' / ('spawn_%d_%s.png' % (i, str(datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S:%f")))))
    
                ego_command = babbling_angle()
                car_command = ego_command[1]
                command = ego_command[0]
    
                env.ego.apply_control(carla.VehicleControl(
                    throttle= car_command[0], steer= car_command[1],
                    brake = car_command[2], reverse = car_command[3]))
    
                motor_output.append(command)
                
        
        i+=1
        
    #saving the motor output to file
    pickle.dump(list(motor_output), motor_output_file)
    #cleaning_up
    env.clean_up()
    motor_output_file.close()
    

if __name__ == "__main__":
    main(sys.argv[1:])
    