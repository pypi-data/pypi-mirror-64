# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 17:33:35 2020

@author: PHULL
"""

import numpy as np
import pandas as pd
import argparse
import sys

def missing_values_fn(file):
    try:
        x=pd.read_csv(file).values
       
    except IOError:
       print ("There was an error reading ", file)
       sys.exit(0)
    x[1,2]=np.nan
    x[4,2]=np.nan
    
    cols=np.size(x,1)
    rows=np.size(x,0)
    
    
    for col in range(cols):
        summ=0
        non_empty_rows=0
        for row in range(rows):
            if(not np.isnan(x[row,col])):
                summ+=x[row,col]
                #print(summ)
                non_empty_rows+=1
        summ=summ/non_empty_rows
        #print("col sum=",summ)
        for r in range(rows):
            if(np.isnan(x[r,col])):
                x[r,col]=summ
                #print("new x",x[r,col])
    
    print("Missing values successully replaced with column average.")
    return x
        

def main():
    parser = argparse.ArgumentParser(prog ='missing_val')
    parser.add_argument("InputDataFile", help="Enter the name of input CSV file with .csv extension",type=str)
    args=parser.parse_args()
    
    sourcefile=args.InputDataFile
     
    data=missing_values_fn(sourcefile)

    pd.DataFrame(data).to_csv(sourcefile)
                #,index=False,header=False)
    
    

if __name__=="__main__":
    main()