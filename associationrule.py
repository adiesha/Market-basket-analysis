import pandas as pd
import numpy as np

from apriori import Xset

class Association():
    
    def __init__(self, f_list, minConf):
        self.f_list = f_list
        self.minConf = minConf
        
    def getAssociation(self):
        c_list = []
        for z in self.f_list:
            if len(z.items) < 2:
                continue
            x = z.powerset()    #create new function to generate single powerset
            A = []
            for item in x:
                A.append(Xset(item))
            
            while len(A) != 0:
                X = A[-1]
                A.remove(X)
                c = z.support / X.support
                if c >= self.minConf:
                    c_list.append((X.items, 'Y', z.support, c))
                else:
                    c_list.append(0)                    
                    #remove A \ W
                    
        return c_list
                
            
# Test file          
f_list = []
f_list.append(Xset(['ABC', 'AB', 'BC']))    
f_list.append(Xset(['AD', 'BD', 'AD']))  

assoc = Association(f_list, 0.9)
c_list = assoc.getAssociation()  


        
            
