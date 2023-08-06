#!/usr/bin/env python

import sys, os
from dosk.yaml_reader import yaml_reader
import argparse 
  
def main(): 
  
    parser = argparse.ArgumentParser(prog ='dock', 
                                     description ='Do Task - The Simple DevOps Task Runner') 
  
    parser.add_argument('task', metavar ='T', nargs ='+', 
                        help ='an integer for the accumulator') 

    parser.add_argument('-local', action ='store_const', const = True, 
                        default = False, dest ='local', 
                        help ="Load local variables") 
  
    args = parser.parse_args()

    yaml_reader.test()
  
    
if __name__ == "__main__":
    main()
