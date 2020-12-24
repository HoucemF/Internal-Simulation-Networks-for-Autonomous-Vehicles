#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 19:15:17 2020

@author: houcem
"""

import pickle
import os, sys, getopt
import glob
import numpy as np

def main(argv):
    
    #Reading arguments
    try:
        opts, args = getopt.getopt(argv, "hp:o:")
    except getopt.GetoptError:
        print("pickle_combiner -p <CSVs path> -o <output path>")
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print ("pickle_combiner -p <CSVs path> -o <output path>")
            sys.exit()
        elif opt == "-p":
            save_path = str(arg)
        elif opt == '-o':
            output_path = str(arg)
            
    result_array = []
    
    os.chdir(save_path)
    
    extension = 'p'
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
    
    for file in all_filenames:
        data = open(file, 'rb+')
        unpickler = pickle.Unpickler(data)
        result_array.append(unpickler.load())
        data.close()
        
    result = result_array[0]
    
    for i in range(1, len(result_array)):
        np.concatenate(result, result_array[i])

if __name__ == "__main__":
    main(sys.argv[1:])