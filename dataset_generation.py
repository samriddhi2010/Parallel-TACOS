import numpy as np
import pandas as pd
import math
from random import randint
import csv


def reading_file(file_name):          # opens the file and appends the values to a list
    file_name = '10' + '/' + file_name
    f = open(file_name)
    v = list()
    for x in f:
        v.append(float(x))
    del v[0]                 # delete first value of the list as the first number in all the generated files is '0' 
    return v , file_name


# Generating Coalitions using Bit Masking technique.

def coalition_strutures(coalition , v):
    k = math.ceil(math.log(len(v) , 2))
    for i in range(1,len(v)+1):
        l = []
        s = bin(i)
        s = s[2:].zfill(k)
        for j in range(0,k):
            if s[j]=='1':
                l.append(k + 1 - (j+1))
        l.sort()
        coalition.append(l)

'''if __name__ == "__main__":
    v = reading_file()
    coalition = list()
    coalition_strutures(coalition,v)
    print(coalition)
    for i in coalition:
        print(i)'''
