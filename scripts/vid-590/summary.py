import pandas as pd
import numpy as np
from log_data import ProcessTwoLogs
import objective_quality as oq
from matplotlib.pyplot import figure, close
import shelve

folder = '../script_results/vid-590'
results = {}
scores = {}
summary_shelve = shelve.open(f'{folder}/summary.shelve')
for codec in ['H264', 'VP8', 'VP9', 'VP9-SVC']:
    loss_to_suffix = {0:'000', 0.005:'005', 0.01:'010', 0.015:'015', 0.02:'020', 0.03:'030', 0.04:'040', 0.05:'050'}
    for loss in [0, 0.005, 0.01, 0.015, 0.02, 0.03, 0.04, 0.05]:
        suffix = codec + loss_to_suffix[loss]
        results[suffix] = ProcessTwoLogs(f'{folder}/sender_{suffix}.log', f'{folder}/receiver_{suffix}.log')
        
        data = results[suffix]
        times_ms = np.array(data.ReceiveStop[pd.notna(data.TS2)].tolist())
        inter_frame_deltas = times_ms[1:] - times_ms[:-1]
        inter_frame_deltas[inter_frame_deltas < 0] = 0
        w, h, fps = oq.GetResolutionAndFramerate(f'{folder}/loss_{suffix}.ivf')
        BRISQUEScore = oq.GetBRISQUEScore(f'{folder}/loss_{suffix}.ivf')
        FramerateScore = oq.GetFramerateScore(fps)
        ResolutionScore = oq.GetResolutionScore(w, h)
        GapsScore = oq.GetGapsScoreFromCaptureTimes(times_ms)
        TotalScore = BRISQUEScore + FramerateScore + ResolutionScore + GapsScore
        scores[suffix] = (BRISQUEScore, FramerateScore, ResolutionScore, GapsScore, TotalScore)
        summary_shelve[f'score_{suffix}'] = scores[suffix]
        summary_shelve[f'frame_deltas_{suffix}'] = inter_frame_deltas
summary_shelve.sync()

for codec in ['H264', 'VP8', 'VP9', 'VP9-SVC']:
    data = summary_shelve[f'frame_deltas_{codec}020']
    fig = figure(figsize=(12, 3))
    ax1 = fig.add_subplot(131)
    ax2 = fig.add_subplot(132)
    ax3 = fig.add_subplot(133)
    ax1.set_title('Inter-frame delay, ms')
    ax1.plot(data, '.')
    ax1.set_xlim(left=0)
    ax1.set_ylim(bottom=0, top=300)
    ax1.set_xlabel('Frame number')
    ax2.set_title('Delay histogram')
    ax2.hist(data, bins=100, histtype='step')
    ax2.set_xlabel('Inter-frame delay, ms')
    ax2.set_xlim(left=0, right=300)
    ax3.set_title('Cumulative Delay distribution')
    ax3.hist(data, bins=100, histtype='step', density=True, cumulative=True)
    ax3.set_xlabel('Inter-frame delay, ms')
    ax3.set_xlim(left=0, right=300)
    ax3.set_ylim(top=1)
    fig.tight_layout()
    fig.suptitle(codec)
    fig.subplots_adjust(top=0.86)
    fig.savefig(f'{folder}/Delays_{codec}.png')

fig = figure(figsize=(6, 4))
ax = fig.add_subplot(111)
ax.set_title('Cumulative Delay distribution')
ax.set_xlabel('Inter-frame delay, ms')
ax.set_xlim(left=0, right=300)
ax.set_ylim(top=1)
for codec in ['H264', 'VP8', 'VP9', 'VP9-SVC']:
    data = summary_shelve[f'frame_deltas_{codec}020']
    ax.hist(data, bins=100, histtype='step', density=True, cumulative=True, label=codec)
ax.legend(loc='lower right')
ax.grid()
fig.tight_layout()
fig.savefig(f'{folder}/CDF.png')

suffixes = ['000', '005', '010', '015', '020', '030', '040', '050']
graph_data = [(0, 'BRISQUE'), (1, 'Framerate'), (2, 'Resolution'), (3, 'Gaps'), (4, 'Total')]
for index, title in graph_data:
    h264_data = [scores['H264' + v][index] for v in suffixes]
    vp8_data = [scores['VP8' + v][index] for v in suffixes]
    vp9_data = [scores['VP9' + v][index] for v in suffixes]
    vp9_svc_data = [scores['VP9-SVC' + v][index] for v in suffixes]
    fig = figure(figsize=(6, 4))
    ax = fig.add_subplot(111)
    ax.plot(range(8), h264_data, '.-', label='H.264')
    ax.plot(range(8), vp8_data, '.-', label='VP8')
    ax.plot(range(8), vp9_data, '.-', label='VP9')
    ax.plot(range(8), vp9_svc_data, '.-', label='VP9-SVC')
    ax.legend()
    ax.set_xticks(range(8))
    ax.set_xticklabels(['0.0 %', '0.5 %', '1.0 %', '1.5 %', '2.0 %', '3.0 %', '4.0 %', '5.0 %'])
    ax.set_xlabel('Loss')
    ax.set_title(title + ' Score')
    fig.tight_layout()
    fig.savefig(folder + '/' + title + ' Score.png')
    # close(fig)
