import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import random
import matplotlib.dates as mdates

def formula():
    data = pd.read_csv(f'data/big_tech/INTU.csv')
    
    max_close = max(data['close'])
    min_close = min(data['close'])
    diff = max_close-min_close
    
    t = 146
    
    slope = (diff/t)
    diff = (max_close-min_close)/2
    starting_point = data['close'][len(data['close'])-1]
    results = []
    count = 0
    for i in range(len(data['close'])-1,0,-1):
        expected_value = starting_point+(slope * count)
        actual_value = data['close'][i]
        kingston = (abs(expected_value-actual_value)/diff)
        
        results.append(kingston)
        
        count+=1
    
        return results


results = formula()

print("SUM OF SCORES : \n",sum(results))