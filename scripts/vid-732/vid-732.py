import pandas as pd
import numpy as np
import math
import pdb
from sklearn.linear_model import LinearRegression as LR
import matplotlib.pyplot as plt

DELAY = 50000 # 50 ms
WINDOW = 10
if True:
    f = open('../../script_results/vid-603/log')
    data = pd.DataFrame(columns=['fb', 'in_flight', 'prioir', 'seq', 'send', 'recv', 'size'], dtype=np.uint64)
    for l in f:
        if 'GOOG-CC-REP' in l:
            feedback_time_us, _, data_in_flight, prior_in_flight = [int(v) for v in l.split()[-4:]]
        elif 'GOOG-CC-FB' in l:
            sequence_number, send_time_us, receive_time_us, size = [int(v) for v in l.split()[-10:-6]]
            data = data.append(dict(fb=feedback_time_us, in_flight=data_in_flight, prioir=prior_in_flight,
                             seq=sequence_number, send=send_time_us, recv=receive_time_us, size=size), ignore_index=True)


def update_probabilities(period, events, weig_coeff):
    period = (period + 500) / 1e6 # as granularity is 1000 us
    A = pow(period, events)/math.factorial(events)
    for i in range(256):
        lam = i * 10000.0/256
        weig_coeff[i] = weig_coeff[i] * A * pow(lam, events) * math.exp(-lam*period)

def normalize_probabilities(weig_coeff):
    su = 0.0
    for i in range(256): su += weig_coeff[i]
    for i in range(256): weig_coeff[i] /= su

def get_lam(weig_coeff):
    su = 0.0
    for j in range(256): su += weig_coeff[j] * j * 10000.0/256
    return su

##%%
## pdb.set_trace()
#weig_coeff = [1/256.0] * 256
#last_fb = 0
#k = 0 # a first packet yet not used to update the model
#L = len(data)
#for i in range(L):
#    current_fb = data.loc[i, 'fb']
#    if current_fb - last_fb >= 20000:
#        # Updating model
#        k2 = k
#        while k2 < L and data.loc[k2, 'fb'] <= current_fb:
#            k2 += 1
#        # now use all packets in range [l, k2)
#        # split by frames, hack with packet size
#        l = k
#        while l < k2:
#            l2 = l
#            s = data.loc[l, 'size']
#            while l2 < k2 and abs(data.loc[l2, 'size'] - s) < 1.5:
#                l2 += 1
#            if l2 - l <= 1:
#                # can't use cases when a frame consists of only one packet
#                l = l2
#                continue
#            # work with [l, l2)
#            period = data.loc[l2 - 1, 'recv'] - data.loc[l, 'recv']
#            events = l2 - 1 - l
#            #print(period, events)
#            update_probabilities(period, events, weig_coeff)
#            #
#            
#            l = l2
#        normalize_probabilities(weig_coeff)
#        print(current_fb - data.loc[0, 'fb'], get_lam(weig_coeff))
#        last_fb = current_fb
#        k = k2

#%%
weig_coeff = [1/256.0] * 256
last_fb = 0
last_known_delay = 0
k = 0 # a first packet yet not used to update the model
L = len(data)
data['est_delay'] = 0.0
data['fact'] = 0.0
data.loc[0, 'est_delay'] = data.loc[0, 'recv'] - data.loc[0, 'send'] # because I can't estimate for fist one
m = 1 # a first packet that yet not has delivery estimate
for i in range(L):
    current_fb = data.loc[i, 'fb']
    if current_fb > last_fb:
        # Updating model
        k2 = k
        while k2 < L and data.loc[k2, 'fb'] <= current_fb:
            k2 += 1
        # now use all packets in range [l, k2)
        # split by frames, hack with packet size
        l = k
        while l < k2:
            l2 = l
            s = data.loc[l, 'size']
            while l2 < k2 and abs(data.loc[l2, 'size'] - s) < 1.5:
                l2 += 1
            if l2 - l <= 1:
                # can't use cases when a frame consists of only one packet
                l = l2
                continue
            # work with [l, l2)
            period = data.loc[l2 - 1, 'recv'] - data.loc[l, 'recv']
            events = l2 - 1 - l
            #print(period, events)
            update_probabilities(period, events, weig_coeff)
            l = l2
        normalize_probabilities(weig_coeff)
        #print(current_fb - data.loc[0, 'fb'], get_lam(weig_coeff))
        # Use lam to estimate delivery times
        lam = get_lam(weig_coeff)
        m2 = m
        while m2 < L and data.loc[m2, 'send'] < current_fb:
            m2 += 1
        # estimate for 
        for j in range(m, m2):
            # WARNING HACK, using 1/6 x lambda
            est_delay = data.loc[last_known_delay, 'recv'] + 1.0e6/(lam/6)*(j - last_known_delay) - data.loc[j, 'send']
            if est_delay < 0:
                est_delay = 0.0
            else:
                real_delay = data.loc[j, 'recv'] - data.loc[j, 'send']
                fact = 1.0e6/lam*(j - last_known_delay)/(real_delay + data.loc[j, 'send'] - data.loc[last_known_delay, 'recv'] )
                data.loc[j, 'fact'] = fact
            data.loc[j, 'est_delay'] = est_delay
        m = m2
        last_fb = current_fb
        last_known_delay = i
        k = k2

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
plt.title('Sprout-like')

plt.figure()
plt.plot(time/1000, x/1000, '.', markersize=1)
plt.xlabel('Playing time, ms')
plt.title('Real delivery time, ms')

# which = data['fact'] != 0
# print('Average factor =', np.average(data.loc[which, 'fact']))