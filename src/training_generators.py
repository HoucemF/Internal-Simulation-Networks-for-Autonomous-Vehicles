#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 01:07:10 2020

@author: houcem
"""

import numpy as np
from imageio import imread
import cv2

def generator(csv_path, batch_size):
    X_train = []
    y_train = []
    batchcount = 0
    
    while True: #Keeping the generator running
        with open(csv_path) as f:
            next(f) #Skipping the header
            for line in f:
                img_x_path, throttle, steering_angle, img_y_path = line.split(',')
                
                #Loading and Normalizing the input frame
                img_x = imread(str(img_x_path))
                img_x = img_x/255.0
                
                #Packing the motor input into a numpy array
                motor_input = np.asarray([throttle, steering_angle])
                
                #Loading and Normalizing the target frame
                #img_y = cv2.imread(img_y_path.rstrip("\n"))
                #img_y = img_y/255.0
                
                #Packing and adding the inputs and targets into the batch
                X_train.append(img_x)
                y_train.append(img_x)
                   
                batchcount += 1    
                    
                if batchcount == batch_size:
                    X_train = np.asarray(X_train)
                    y_train = np.asarray(y_train)
                    yield(X_train, y_train)
                    X_train = []
                    y_train = []
                    batchcount = 0
                    

def babbling_generator(csv_path, batch_size):
    X_train = []
    y_train = []
    motor_train = []
    batchcount = 0
    
    while True: #Keeping the generator running
        with open(csv_path) as f:
            next(f) #Skipping the header
            for line in f:
                img_x_path, throttle, steering_angle, img_y_path = line.split(',')
                
                #Loading and Normalizing the input frame
                img_x = imread(str(img_x_path))
                img_x = img_x/255.0
                
                #Packing the motor input into a numpy array
                motor_input = np.asarray([float(throttle), float(steering_angle)])
                
                #Loading and Normalizing the target frame
                img_y = cv2.imread(str(img_y_path).rstrip("\n"))
                img_y = img_y/255.0
                
                #Packing and adding the inputs and targets into the batch
                X_train.append(img_x)
                motor_train.append(motor_input)
                y_train.append(img_y)
                   
                batchcount += 1    
                    
                if batchcount == batch_size:
                    X_train = np.asarray(X_train)
                    motor_train = np.asarray(motor_train)                    
                    y_train = np.asarray(y_train)
                    yield([X_train, motor_train], y_train)
                    X_train = []
                    y_train = []
                    motor_train = []
                    batchcount = 0
                    
def train_generator(csv_path, batch_size):
    X_train = []
    batchcount = 0
    
    while True: #Keeping the generator running
        with open(csv_path) as f:
            next(f) #Skipping the header
            for line in f:
                img_x_path, throttle, steering_angle, img_y_path = line.split(',')
                
                #Loading and Normalizing the input frame
                img_x = imread(str(img_x_path))
                img_x = img_x/255.0
                
                #Packing the motor input into a numpy array
                motor_input = np.asarray([throttle, steering_angle])
                
                #Loading and Normalizing the target frame
                #img_y = cv2.imread(img_y_path.rstrip("\n"))
                #img_y = img_y/255.0
                
                #Packing and adding the inputs and targets into the batch
                X_train.append(img_x)
                   
                batchcount += 1    
                    
                if batchcount == batch_size:
                    X_train = np.asarray(X_train)
                    yield(X_train)
                    X_train = []
                    batchcount = 0
                    
def train_y_generator(csv_path, batch_size):
    y_train = []
    batchcount = 0
    
    while True: #Keeping the generator running
        with open(csv_path) as f:
            next(f) #Skipping the header
            for line in f:
                img_x_path, throttle, steering_angle, img_y_path = line.split(',')
                
                #Loading and Normalizing the input frame
                #img_x = imread(str(img_x_path))
                #img_x = img_x/255.0
                
                #Packing the motor input into a numpy array
                motor_input = np.asarray([throttle, steering_angle])
                
                #Loading and Normalizing the target frame
                img_y = cv2.imread(img_y_path.rstrip("\n"))
                img_y = img_y/255.0
                
                #Packing and adding the inputs and targets into the batch
                y_train.append(img_y)
                   
                batchcount += 1    
                    
                if batchcount == batch_size:
                    y_train = np.asarray(y_train)
                    yield(y_train)
                    y_train = []
                    batchcount = 0
                    
def motor_parser(csv_path):
    motor_input = []
    f = open(csv_path)
    next(f)
    for line in f:
        img_x_path, throttle, steering_angle, img_y_path = line.split(',')
        motor_input.append(np.asarray([throttle, steering_angle]))
    return np.asarray(motor_input)        