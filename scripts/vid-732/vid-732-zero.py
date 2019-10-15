#%% Imports
import pandas as pd
import numpy as np
import math
import pdb
from sklearn.linear_model import LinearRegression as LR
import matplotlib.pyplot as plt

##%% Data input
#DELAY = 50000 # 50 ms
#WINDOW = 10
#if True:
#    f = open('../../script_results/vid-603/log')
#    data = pd.DataFrame(columns=['fb', 'in_flight', 'prioir', 'seq', 'send', 'recv', 'size'], dtype=np.uint64)
#    for l in f:
#        if 'GOOG-CC-REP' in l:
#            feedback_time_us, _, data_in_flight, prior_in_flight = [int(v) for v in l.split()[-4:]]
#        elif 'GOOG-CC-FB' in l:
#            sequence_number, send_time_us, receive_time_us, size = [int(v) for v in l.split()[-10:-6]]
#            data = data.append(dict(fb=feedback_time_us, in_flight=data_in_flight, prioir=prior_in_flight,
#                             seq=sequence_number, send=send_time_us, recv=receive_time_us, size=size), ignore_index=True)

#%% Estimate
weig_coeff = [1/256.0] * 256
last_fb = 0
last_known_delay = 0
L = len(data)
data['est_delay'] = 0.0
data.loc[0, 'est_delay'] = data.loc[0, 'recv'] - data.loc[0, 'send'] # because I can't estimate for fist one
m = 1 # a first packet that yet not has delivery estimate
for i in range(L):
    current_fb = data.loc[i, 'fb']
    if current_fb > last_fb:
        m2 = m
        while m2 < L and data.loc[m2, 'send'] < current_fb:
            m2 += 1
        est_delay = data.loc[last_known_delay, 'recv'] - data.loc[last_known_delay, 'send']
        for j in range(m, m2):
            data.loc[j, 'est_delay'] = est_delay
        m = m2
        last_fb = current_fb
        last_known_delay = i

# Trend - clock skew
#       0 -> 66.8
# 160 000 -> 151.5
#%% Plotting
which = data['est_delay'] != 0
x = np.array(data.loc[which, 'recv'] - data.loc[which, 'send']).astype(np.float64)
time = np.array(data.loc[which, 'send'] - data.loc[data[which].index[0], 'send']).astype(np.float64)
x -= 0.53e-3*time
y = np.array(data.loc[which, 'est_delay'])
y -= 0.53e-3*time
print('Correlation =', np.corrcoef(x, y)[0][1])
plt.plot(x/1000, y/1000, '.', markersize=1)
MAX=200
plt.plot([0, MAX], [0, MAX], markersize=1)
plt.xlim(0, MAX)
plt.ylim(0, MAX)
plt.xlabel('Real delivery time, ms')
plt.ylabel('Predicted delivery time. ms')
plt.title('Last delay model')

# plt.figure()
# plt.plot(time/1000, x/1000, '.', markersize=1)
# plt.xlabel('Playing time, ms')
# plt.title('Real delivery time, ms')
