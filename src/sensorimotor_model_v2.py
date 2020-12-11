#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 23:27:29 2020

@author: houcem
"""

"""
This class defines the model
and loads its pretrained weights
"""

from tensorflow import keras
from keras.layers import Conv2D, Dense, Concatenate, BatchNormalization, Input, MaxPooling2D, Flatten, Reshape, UpSampling2D
from keras.activations import selu
from keras import Model

class sensorimotor_model_v2:
    
    def __init__(self):
        self.encoder = self.make_encoder()
        self.decoder = self.make_decoder()
        self.mapping_mlp = self.make_mapping_mlp()
        self.model = self.make_model(self.encoder, self.decoder, self.mapping_mlp)


    #Create the encoder
    def make_encoder(self):
        image_input = Input(shape=(112,112,3))
        x = Conv2D(8, (3,3), activation = selu, padding = 'same', use_bias = False, kernel_initializer=keras.initializers.he_uniform())(image_input)
        x = BatchNormalization()(x)
        x = MaxPooling2D()(x)
        x = Conv2D(16, (3,3), activation = selu, padding = 'same', use_bias = False, kernel_initializer=keras.initializers.he_uniform())(x)
        x = BatchNormalization()(x)
        x = MaxPooling2D()(x)
        x = Conv2D(32, (3,3), activation = selu, padding = 'same', use_bias = False, kernel_initializer=keras.initializers.he_uniform())(x)
        x = BatchNormalization()(x)
        x = MaxPooling2D()(x)
        x = Conv2D(64, (3,3), activation = selu, padding = 'same', use_bias = False, kernel_initializer=keras.initializers.he_uniform())(x)
        x = BatchNormalization()(x)
        x = MaxPooling2D()(x)
        x = Flatten()(x)
        
        z = Dense(128, activation = 'sigmoid')(x)
        
        encoder = Model(inputs= [image_input], outputs = [z])
        
        return(encoder)
    
    #Create the Decoder
    def make_decoder(self):
        input_decoder = Input(shape=(128,))

        dense_1= Dense(3136, activation = selu, activity_regularizer = keras.regularizers.l2(1e-4), kernel_initializer=keras.initializers.he_uniform())(input_decoder)
        d = Reshape((7,7,64))(dense_1)
        d = UpSampling2D()(d)
        d = Conv2D(64,(3, 3), strides=1, activation= selu, padding='same', use_bias = False, kernel_initializer=keras.initializers.he_uniform())(d)
        d = BatchNormalization()(d)
        d = UpSampling2D()(d)
        d = Conv2D(32,(3, 3), strides=1, activation= selu, padding='same', use_bias = False, kernel_initializer=keras.initializers.he_uniform())(d)
        d = BatchNormalization()(d)
        d = UpSampling2D()(d)
        d = Conv2D(16,(3, 3), strides=1, activation= selu, padding='same', use_bias = False, kernel_initializer=keras.initializers.he_uniform())(d)
        d = BatchNormalization()(d)
        d = UpSampling2D()(d)
        d = Conv2D(8,(3, 3), strides=1, activation= selu, padding='same', use_bias = False, kernel_initializer=keras.initializers.he_uniform())(d)
        d = BatchNormalization()(d)
        decoded = Conv2D(3, (3, 3), strides = 1, activation='linear', padding='same')(d)

        
        Decoder = Model(inputs = input_decoder, outputs = decoded)
        
        return Decoder
    
    #Create the Mapping mlp
    def make_mapping_mlp(self):
        latent_input = Input(shape=(128,))

        motor_input = Input(shape=(2,))
        
        babbling_input = Concatenate()([latent_input, motor_input])
        
        z = Dense(512, activation = selu, activity_regularizer= keras.regularizers.l2(1e-4), kernel_initializer = keras.initializers.he_uniform())(babbling_input)
        z = Dense(128, activation = 'sigmoid')(z)
        
        babbling_mlp = Model(inputs = [latent_input, motor_input], outputs = z)
        
        return babbling_mlp
    
    #Create the full model
    def make_model(self, encoder, decoder, mapping_mlp):
        img_input = Input(shape=(112, 112, 3), name = "img")
        motor_input = Input(shape=(2,), name = "motor")
        
        Encoded = encoder([img_input])
        babbling = mapping_mlp([Encoded, motor_input])
        Decoded = decoder(babbling)
        
        babbling_model = Model(inputs = [img_input, motor_input], outputs = Decoded)
        
        return(babbling_model)
               
        
