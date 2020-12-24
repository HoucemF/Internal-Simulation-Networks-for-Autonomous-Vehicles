#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 21:13:07 2020

@author: houcem
"""

from sensorimotor_model_v2 import sensorimotor_model_v2
from scipy.spatial.distance import euclidean, cosine, correlation
from sim_env import Sim_env
from camera import Camera
import carla
from cv2 import imread
import numpy as np
from skimage.measure import compare_mse, compare_ssim
import sys
import getopt
from pathlib import Path

def autoregressive_filter(previous_angle, best_angle, alpha):
    return alpha * best_angle + (1 - alpha) * previous_angle

def main(argv):
    
    alpha = 0.9
    
    #Reading arguments
    try:
        opts, args = getopt.getopt(argv, "he:w:r:a:")
    except getopt.GetoptError:
        print("driver -w <Weights path> -r <Reference image path> -a <Alpha value>")       
        sys.exit(2)
        
    for opt, arg in opts:
        if opt == '-h':
             print ("driver -w <Weights path> -r <Reference image path> -a <Alpha value>")    
             sys.exit()
        elif opt == "-w":
             weights_path = str(arg)
        elif opt == "-r":
             ref_path = str(arg)
        elif opt == "-a":
             alpha = float(arg)
    
    #Defining the model
    models = sensorimotor_model_v2()
    
    #Path to weights
    weights_path = weights_path
    
    #Applying the weights
    models.encoder.trainable = False
    models.model.load_weights(weights_path)
    print("Weights Loaded")
        
    #Specifying the models
    model = models.model
    encoder = models.encoder
    mlp = models.mapping_mlp
        
    #Reference Image
    ref = imread(ref_path)
    ref = ref/255.0
    ref = ref.reshape([112,112,3])
    ref_vector = encoder.predict(ref.reshape([1,112,112,3]))
    print("reference image loaded")
    
    env = Sim_env(town = "Town03")
    env.spawn_ego(spawn_point = 6)
    print("Vehicle Spawned")
    rgb_camera = Camera(env.world, env.blueprints, env.ego, False)
    spectator = env.world.get_spectator()
    spectator.set_transform( carla.Transform(
                env.ego.get_location() + carla.Location(z=50),
                carla.Rotation(pitch=-90)))
    
    env.enter()
    print("entering the matrix")
    
    angles = [-0.5, -0.45, -0.4, -0.35, -0.3, -0.25, -0.2, -0.15, -0.10, -0.05, 0,
                  0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5]
    
    i = 0
    previous_angle = 0
    
    while(True):
        env.world.tick()
        
        spectator.set_transform( carla.Transform(
                env.ego.get_location() + carla.Location(z=50),
                carla.Rotation(pitch=-90)))
        
   
    
        image = None
        
        angles_score = dict.fromkeys(angles)       
                    
        while image is None and rgb_camera.queue.qsize() > 0:
            image = rgb_camera.get()
            image = image/255.0
            image = image.reshape([1,112,112,3])
        
        image_vec = encoder.predict(image)
            
        
        for angle in angles:
            motor_command = np.asarray([0.2, angle])  
            motor_command = motor_command.reshape([1,2])
            imagined_vec = mlp.predict([image_vec, motor_command]) 
            angles_score[angle] = correlation(imagined_vec, ref_vector)
            
            
        best_angle = max(angles_score, key = angles_score.get)
        driving_angle = autoregressive_filter(previous_angle , best_angle , alpha)
        print(driving_angle)
        
        env.ego.apply_control(carla.VehicleControl(throttle = 0.2, steer = driving_angle, brake = 0, reverse = 0))
        previous_angle = driving_angle
        
        i = i+1

if __name__ == "__main__":
    main(sys.argv[1:])
    