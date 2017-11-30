# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 21:07:26 2017
plot positive and negative sentiment scores vs stock price 
since stock price and sentiment scores are not in the same scale
the stock prices are divided by a large integer
- Chipotle CMG 2015 stock price values are scaled down by 9000
- Chipotle CMG 2017 stock price values are scaled down by 4000 
- Taco Bell YUM 2015 stock price values are scaled down by 800
- Taco Bell YUM 2017 stock price values are scaled down by 1000

@author: Carrie
"""

import pandas as pd  # DataFrame structure and operations
import matplotlib.pyplot as plt  # 2D plotting
import os
import numpy as np

os.listdir(".")
in_filename = 'plot_data_4_files/chipotle2017_plot_data.csv'
out_filename = 'fig_CMG_chipotle_stock_price_2017.pdf'
df = pd.read_csv(in_filename)
print(df)
print(df.describe())
print('\nCorrelation between positive score and stock_price',\
    round(df['positive_score'].corr(df['stock_price']),3))
print('\nCorrelation between negative score and stock_price',\
    round(df['negative_score'].corr(df['stock_price']),3))

plt.figure()
t = np.arange(0,92,1)
# get sentiment scores
pos = df['positive_score'].values.tolist()
neg = df['negative_score'].values.tolist()
# get stock price
stk = np.array(df['stock_price'].values.tolist())
# scale down stock price for comparison
s3 = stk/4000
np_s = np.array(neg) - np.array(pos)
plt.plot(t, pos,'b--',linewidth=0.5)
plt.plot(t, neg, 'r--', linewidth=0.5)
plt.plot(t, s3, 'g-', linewidth=2.0)
plt.legend(['pos', 'neg', 'stock'], loc='lower left')
plt.title('positive & negative sentiment vs. CMG stock price')
plt.xlabel('days from 8/1/2017 - 10/31/2017 (Chipotle)')
plt.ylabel('sentiment scores & stock price') 
plt.grid()
# plt.show() 
# save figure to file 
plt.gcf()
plt.savefig(out_filename,
    bbox_inches = 'tight', dpi=None, facecolor='none', edgecolor='blue', 
    orientation='portrait', papertype=None, format=None, 
    transparent=True, pad_inches=0.25, frameon=None)  

