import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

plt.rcParams['figure.figsize'] = [20, 15]
df = pd.read_csv('filtered.txt', sep='\t')

df.set_index('time')
df