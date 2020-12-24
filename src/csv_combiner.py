#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 18:39:41 2020

@author: houcem
"""

import os, sys, getopt
import glob
import pandas as pd

"""
This script requires you to put all the csvs generated
in one folder and it will combine all the csvs into one csv
and outputs a csv a specified directory
"""

def main(argv):
    
    #Reading arguments
    try:
        opts, args = getopt.getopt(argv, "hp:o:")
    except getopt.GetoptError:
        print("csv_combiner -p <CSVs path> -o <output path>")
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print ("csv_combiner -p <CSVs path> -o <output path>")
            sys.exit()
        elif opt == "-p":
            save_path = str(arg)
        elif opt == '-o':
            output_path = str(arg)
            
    os.chdir(save_path)
    os.mkdir(output_path)
    
    extension = 'csv'
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
    
    #combine all files in the list
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
    #export to csv
    combined_csv.to_csv( output_path + "/combined_csv.csv", index=False)
    
if __name__ == "__main__":
    main(sys.argv[1:])