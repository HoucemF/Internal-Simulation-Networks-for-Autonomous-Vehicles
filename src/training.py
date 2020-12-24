#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 01:20:07 2020

@author: houcem
"""

"""
This is the training script for the 
motor babbling experiment, it takes as input the path
to the validation and training csv, the path to the
pickle file containing the motor inputs and a flag that 
says which network to freeze during training
"""
import sys
import getopt
import pickle

from training_generators import *
from sensorimotor_model_v2 import sensorimotor_model_v2
import tensorflow.keras as keras
import tensorflow as tf
from datetime import datetime
from pathlib import Path

#Custom loss function
def SSIM_l1_loss(y_true, y_pred):
    return 1 - tf.reduce_mean(tf.image.ssim_multiscale(y_true,y_pred, max_val=1, filter_size=3)) + keras.losses.mae(y_true, y_pred)

def main(argv):
    
    batch_size = 50
    train_csv_path = "/home/houcem/data/combined_csv.csv"
    val_csv_path = "/home/houcem/data_val/data.csv"
    flag = 2
    save_path = "/home/houcem/"
    

    #Reading arguments
    try:
        opts, args = getopt.getopt(argv, "ht:e:f:s:")
    except getopt.GetoptError:
        print("training -t <path to training csv> -e <path to evaluation csv> -f <0 : Nothing frozen 1: Freezes Encoder 2: Freezes Encoder and Decoder> -s <save_path>")       
        sys.exit(2)
        
    for opt, arg in opts:
        if opt == '-h':
             print("training -t <path to training csv> -e <path to evaluation csv> -f <0 : Nothing frozen 1: Freezes Encoder 2: Freezes Encoder and Decoder> -s <save_path>")       
             sys.exit()
        elif opt == "-t":
             train_csv_path = str(arg)
        elif opt == "-e":
             val_csv_path = str(arg)
        elif opt == "-f":
             flag = int(arg)
        elif opt == "-s":
             save_path = str(arg)
                 
    train_sample_size = sum(1 for row in open(train_csv_path)) - 1
    val_sample_size = sum(1 for row in open(val_csv_path)) - 1            
    models = sensorimotor_model_v2()
    
    
    """
    Training the autoencoder
    """
    print('compiling autoencoder')
    models.autoencoder.compile(loss = SSIM_l1_loss, optimizer = keras.optimizers.Adam(learning_rate=1e-3))
    
    tensorboard = keras.callbacks.TensorBoard(log_dir='./logs', histogram_freq=1)
    models.autoencoder.fit(generator(train_csv_path, batch_size), steps_per_epoch = train_sample_size/batch_size, epochs = 40, validation_data= generator(val_csv_path, batch_size), validation_steps= val_sample_size/batch_size, callbacks= [tensorboard])
    print('autoencoder training done')
    
    
    """
    Preparing data for the mapping network
    """
    print('vectorizing for the mapping network')
    print('vectorizing the input images')
    print("...")
    train_X = models.encoder.predict(train_generator(train_csv_path, batch_size), steps = train_sample_size/batch_size)
    print("...")
    train_X = train_X[0:train_sample_size,:]
    
    print('vectorizing the target images')
    print("...")
    train_y = models.encoder.predict(train_y_generator(train_csv_path, batch_size), steps = train_sample_size/batch_size)
    print("...")
    train_y = train_y[0:train_sample_size,:]

    print('loading motor data')
    training = motor_parser(train_csv_path)
    
    training = np.asarray(training)    

    """
    training the mapping network
    """    
    print("compiling the model")
    models.mapping_mlp.compile(loss = 'mse', optimizer = keras.optimizers.Adam(learning_rate=1e-4))
    
    print("starting the training of the mapping network")
    models.mapping_mlp.fit(x=[train_X, training], y= train_y, epochs=5)
    
    
    if flag == 1:
        print('freezing encoder')
        models.encoder.trainable = False
    else:
        if flag == 2:
            print("freezing encoder and decoder")
            models.encoder.trainable = False
            models.decoder.trainable = False
            
        else:
            print('nothing frozen')

    print('training the babbling network')
    models.model.compile(loss = SSIM_l1_loss, optimizer = keras.optimizers.Adam(learning_rate = 1e-4))
    models.model.fit(babbling_generator(train_csv_path, batch_size), steps_per_epoch= train_sample_size/batch_size, validation_data=babbling_generator(val_csv_path,batch_size), validation_steps=val_sample_size/batch_size, epochs = 10)
    
    models.encoder.trainable = False
    models.decoder.trainable = True
    
    print("saving the weights in the execution directory")
    models.model.save_weights('%s.h5' % str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")))
    
    
if __name__ == "__main__":
    main(sys.argv[1:])