import pandas as pd
import numpy as np
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

data['est_delay'] = 0.0
L = len(data)
lr = LR()
for i in range(L):
    send = float(data.loc[i, 'send'])
    j = i - 1
    found = False
    while (not found) and j >= WINDOW:
        if data['fb'][j] + DELAY < send:
            found = True
        else:
            j -= 1
    if found:
        x = np.array(data['send'][j-WINDOW+1:j+1]).reshape(-1,1)
        y = np.array(data['recv'][j-WINDOW+1:j+1]).reshape(-1,1) - x
        t = lr.fit(x.astype(np.float64), y.astype(np.float64)).predict([[send]])[0][0]
        data.loc[i, 'est_delay'] = t if t > 0 else 0
which = data['est_delay'] != 0
x = np.array(data.loc[which, 'recv'] - data.loc[which, 'send']).astype(np.float64)
y = np.array(data.loc[which, 'est_delay'])
print(np.corrcoef(x, y))
plt.plot(x/1000, y/1000, '.', markersize=1)
MAX=200
plt.plot([0, MAX], [0, MAX], markersize=1)
plt.xlim(0, MAX)
plt.ylim(0, MAX)
plt.xlabel('Real delivery time, ms')
plt.title('Predicted delivery time. ms')

plt.figure()
y = data.loc[which, 'send'] - data.loc[data[which].index[0], 'send']
plt.plot(y/1000, x/1000, '.', markersize=1)
plt.xlabel('Playing time, ms')
plt.title('Real delivery time, ms')
