#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 18:39:41 2020

@author: houcem
"""

import os
import glob
import pandas as pd
os.chdir("/home/houcem/data")

extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

#combine all files in the list
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
#export to csv
combined_csv.to_csv( "/home/houcem/data/combined_csv.csv", index=False)