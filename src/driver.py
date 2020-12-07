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

def autoregressive_filter(previous_angle, best_angle, alpha):
    return alpha * best_angle + (1 - alpha) * previous_angle

def main():
    
    #Defining the model
    models = sensorimotor_model_v2()
    
    #Path to weights
    weights_path = "/home/houcem/Houcem/experimentation/babbling_model_babbling_SSIM.h5"
    
    #Applying the weights
    models.model.load_weights(weights_path)
    print("Weights Loaded")
        
    #Specifying the models
    model = models.model
    encoder = models.encoder
    mlp = models.mapping_mlp
    
    #Reference Image
    ref = imread("/home/houcem/Documents/Motor Babbling/src/reference_image1.png")
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
            angles_score[angle] = cosine(imagined_vec, ref_vector)
            
            
        best_angle = max(angles_score, key = angles_score.get)
        driving_angle = autoregressive_filter(previous_angle , best_angle , 0.1)
        print(driving_angle)
        
        env.ego.apply_control(carla.VehicleControl(throttle = 0.2, steer = driving_angle, brake = 0, reverse = 0))
        previous_angle = driving_angle
        
        i = i+1

if __name__ == "__main__":
    main()