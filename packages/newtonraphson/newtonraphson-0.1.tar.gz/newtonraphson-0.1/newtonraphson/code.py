import numpy as np
import math

class Newton:
    
    def __init__(self,degree,coeff,approx):        
        poly_degree=np.linspace(0,degree,degree+1)
        self.degree=poly_degree
        self.coeff=coeff
        self.approx=approx
        
    def calculate_value(self,x):
        value=0
        for i in range(0,len(self.degree)):
            value+=self.coeff[i]*math.pow(x,self.degree[i])
        return value  


    
    def calculate_value_diff(self,x,power):
        degree=self.degree
        coeff = self.coeff
        for i in range(1,power+1):
            coeff = np.multiply(coeff,degree)
            degree= degree-1
            degree= degree*np.array([i for i in degree>=0])        
        value=0
        for i in range(0,len(degree)):
            value+=coeff[i]*math.pow(x,degree[i])
        return value
    
    def calculate_root(self,x):
        i=1
        while True:
            xprec=x
            x=x-self.calculate_value(x)/self.calculate_value_diff(x,i)            
            if(xprec==x):
                break
        return round(x,self.approx)