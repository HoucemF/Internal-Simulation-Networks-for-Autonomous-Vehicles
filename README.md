# Houcem

The folder src contains code that is written and tested.\
The folder experimentation has exploratory code or a work in progress

# Instructions

These instructions are for ubuntu 18.04 and suppose that you use the anaconda/miniconda package manager

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
## Data collection guide

There are two scripts to collect rgb images, segmented images and the associated steering angles and throttles from the simulation. 

### Script 1: Using Auto-pilot
This script uses autopilot to drive around the map staying within its lane but ignoring road signs and traffic lights.
```
python src/data_collection.py -p <Save path> -e <number of episodes> -f <number of frames skipped>
```
### Script 2: Using Babbling
The car is spawned to move randomly in the city for 250 episodes with a frame skip of 5 then it is respawned elsewhere in the map. The process continues until the car visits every spawn point in the map
```
python src/data_collection_angle.py -p <Save path> 
```

After using the scripts to collect data, some preprocessing is needed to create a csv that is used for training the models, run build_csv.py to get the final csv for it

```
python src/build_csv -p <Directory of the saved data>
```

To preprocess the data that is coming from the babbling process use 
```
python src/build_csv_babbling -p <Directory of the saved data>
```

## Training Guide
TODO

# Execution Guide

To execute the work, first run carla using
```
./CarlaUE4.sh -quality-level=Low
```
Then execute the driver script 
```
python src/driver.py -w <Weights path> -r <Reference image path> -a <Alpha value>
```
