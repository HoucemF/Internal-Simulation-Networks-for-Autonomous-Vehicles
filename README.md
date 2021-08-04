# Project Overview and Scope

This project is made for ECE591 - Directed Studies Module under the advisorship of Dr. Jaerock Kwon in BIMILab at the University of Michigan - Dearborn. The goal of the project is to predict the next frame vector seen by the vehicle using the current frame and the motor action taken by the vehicle. We use this mechanism for a lane keeping application that uses a grid search on a range of steering angles and compares the predicted frame vector to a reference vector using the cosine similarity metric. We use an autoencoder for vectorization of the images and a multi-layer perceptron to predict the next frame vectors.

# Folders Structure

The folder src contains code that is written and tested.\
The folder experimentation has exploratory code or a work in progress \
The Models folder contains the trained neural networks in Keras and Tensorflow \
The environment folder contains a yaml file that can load the work environment in Anaconda \

# Instructions

These instructions are for Ubuntu 18.04 and suppose that you use the anaconda/miniconda package manager

## Installation Guide
First of all, create an environment using the yaml file in environments, this environment uses Python 3.7
```
conda env create -f carla.yml
```
Then, download Carla version 0.9.10.1 using the following link https://github.com/carla-simulator/carla/releases/tag/0.9.10.1

Finally, to be set and start using the carla PythonAPI, go to where you installed Carla
```
cd PythonAPI/carla/dist

easy_install carla-0.9.10-py3.7-linux-x86_64.egg
```

## Definitions
Episode: A Carla episode is a simulation sequence where the vehicle applies a form of control and captures the input from the sensors and then allows the simulation to run for a finite time period

Frame_skip (collection rate/frequency): is the frequency of frames when the data is collected. If frame_skip = 1, the script will attempt to collect the motor command and the image at every frame

## Data collection guide

There are two scripts to collect rgb images, segmented images and the associated steering angles and throttles from the simulation. 

### Script 1: Using Auto-pilot
This script uses autopilot to drive around the map staying within its lane but ignoring road signs and traffic lights. For trial purposes, let's collect a toy dataset of 1000 episodes and by default the number of frames skipped is 1 (No frames skipped). It is recommended that you add at least 4 frames skipped.
```
python src/data_collection.py -p <Save path> -e <number of episodes> -f <number of frames skipped>
```
### Script 2: Using Babbling
The car is spawned to move randomly in the city for 250 episodes with a frame skip of 5 then it is respawned elsewhere in the map. The process continues until the car visits every spawn point in the map
```
python src/data_collection_babbling.py -p <Save path> 
```

After using the scripts to collect data, some preprocessing is needed to create a csv that is used for training the models, run build_csv.py to get the final csv for it. You can add additional frame_skip here if you want. In here, 0 is for no frame_skip (recommended).

```
python src/build_csv -p <Directory of the saved data> -f <frame_skip>
```

To preprocess the data that is coming from the babbling process use 
```
python src/build_csv_babbling -p <Directory of the saved data> 
```

## Training Guide

To train the model, all you have to do is run the following 
```
training -t <path to training csv> -e <path to evaluation csv> -f <0 : Nothing frozen 1: Freezes Encoder 2: Freezes Encoder and Decoder> -s <save_path>
```

# Execution Guide

To execute the work, first run carla using
```
./CarlaUE4.sh -quality-level=Low
```
Then execute the driver script and load Models/Model_v2.h5. There are three reference images in src that can be used. Alpha is a value that gives more importance to the current output of the model compared with the past input
```
python src/driver.py -w <Weights path> -r <Reference image path> -a <Alpha value>
```
#Demo GIFs

Some Bird Eye vue images of the vehicle in different situations

![Car straight lane](https://user-images.githubusercontent.com/72029066/128208791-9e372844-3abf-4d75-955a-871412ba81d9.gif)

![Intersection](https://user-images.githubusercontent.com/72029066/128210684-09b41e46-6281-4e6e-ac70-27f5ed06a416.gif)
