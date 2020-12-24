#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 10:27:04 2020

@author: houcem
"""

from glob import glob
import pandas as pd
from pathlib import Path
import pickle
import sys
import getopt
from datetime import datetime


"""
This class compiles the data into a CSV
for use by a generator.
It expects a folder path containing a pickle file
and a folder called rgb containing the images
"""

class build_csv:
    
    """
    Gets the pickled motor data
    and a list of paths for the images
    """
    def read_data(self, path):
        
        #Reading Motor Data from pickle file
        motor_file = open(Path(path / 'motor_output.p'), 'rb+')
        motor_unpickler = pickle.Unpickler(motor_file)
        motor_data = motor_unpickler.load()
        
        #Cleaning up
        motor_file.close()
        
        #Getting the paths of the images
        image_paths = sorted(glob(str(path/ 'rgb/*.png')))
        
        return motor_data, image_paths
    
    """
    Aggregates the data in a CSV file
    """
    def data_2_csv(self, path, motor_data, image_paths):
        
        #create an empty dataframe
        data = pd.DataFrame(columns = ['img_x', 'throttle', 'steer', 'img_y'])
        
        #Append the data to a dataframe
        for i in range(len(image_paths)-1):
            if "_0049" not in image_paths[i]:
                data = data.append({'img_x' : image_paths[i], 'throttle' : motor_data[i][0],
                                    'steer' : motor_data[i][1], 'img_y' : image_paths[i+1]},
                                   ignore_index=True)
        
        #Export the data to a csv
        data.to_csv(str(path/ ('%s.csv' % (str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f"))))), index= False)
        
    def __init__(self, path):
        
        self.path = Path(path)
        self. motor_data, self.image_paths = self.read_data(self.path)
        self.data_2_csv(self.path, self.motor_data, self.image_paths)
        
        return 
    

def main(argv):
    path = Path("/home/houcem/data_val/")

    
    #Reading arguments
    try:
        opts, args = getopt.getopt(argv, "hp:")
    except getopt.GetoptError:
        print("build_csv -p <Save path>")       
        sys.exit(2)
        
    for opt, arg in opts:
        if opt == '-h':
             print ("build_csv -p <Save path>")    
             sys.exit()
        elif opt == "-p":
             path = Path(arg)
       
    csv_builder = build_csv(path)
    
if __name__ == "__main__" :
    main(sys.argv[1:]);