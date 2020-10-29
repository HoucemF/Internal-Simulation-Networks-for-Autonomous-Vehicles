#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 17:41:26 2020

@author: houcem
"""

import carla
from queue import Queue
from img_utils import carlaimg_to_numpy

"""
This class defines the camera actor
its parameters and the actor it is
attached to
"""

class Camera:
    
    """
    We define the constructor
    for the camera, it can define its
    different parameters. You can choose 
    between a segmented image and a regular 
    image
    """
    
    def __init__(self, world, blueprints, ego, segmentation ,resx=112, resy=112, fov=90):
        self.segmentation = segmentation
        if self.segmentation == True:
            camera_bp = blueprints.find('sensor.camera.semantic_segmentation')
            print('sensor.camera.semantic_segmentation')
        else:
            camera_bp = blueprints.find('sensor.camera.rgb')

        
        camera_bp.set_attribute("image_size_x",str(resx))
        camera_bp.set_attribute("image_size_y",str(resy))
        camera_bp.set_attribute('fov', str(fov))
        
        self.queue = Queue()
        self.camera = world.spawn_actor(camera_bp, carla.Transform(carla.Location(x=2.5, z=1.7), carla.Rotation(pitch= -45)) , attach_to = ego)
        self.camera.listen(lambda img : self.queue.put(carlaimg_to_numpy(img, self.segmentation)))
        
    def get(self):
        image = None
        
        while image is None or self.queue.qsize() > 0:
            image = self.queue.get()
            
        return image