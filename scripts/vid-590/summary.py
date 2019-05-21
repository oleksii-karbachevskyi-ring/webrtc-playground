import pandas as pd
import numpy as np
from log_data import ProcessTwoLogs
import objective_quality as oq
from matplotlib.pyplot import figure, close

folder = '../script_results/vid-590'
results = {}
scores = {}
for codec in ['H264', 'VP8', 'VP9', 'VP9-SVC']:
    loss_to_suffix = {0:'000', 0.005:'005', 0.01:'010', 0.015:'015', 0.02:'020', 0.03:'030', 0.04:'040', 0.05:'050'}
    for loss in [0, 0.005, 0.01, 0.015, 0.02, 0.03, 0.04, 0.05]:
        suffix = codec + loss_to_suffix[loss]
        results[suffix] = ProcessTwoLogs(f'{folder}/sender_{suffix}.log', f'{folder}/receiver_{suffix}.log')
        
        data = results[suffix]
        capture_times_ms = np.array(data.CaptureTime[pd.notna(data.TS2)].tolist())
        inter_frame_deltas = capture_times_ms[1:] - capture_times_ms[:-1]
        w, h, fps = oq.GetResolutionAndFramerate(f'{folder}/loss_{suffix}.ivf')
        BRISQUEScore = oq.GetBRISQUEScore(f'{folder}/loss_{suffix}.ivf')
        FramerateScore = oq.GetFramerateScore(fps)
        ResolutionScore = oq.GetResolutionScore(w, h)
        GapsScore = oq.GetGapsScoreFromCaptureTimes(capture_times_ms)
        TotalScore = BRISQUEScore + FramerateScore + ResolutionScore + GapsScore
        scores[suffix] = (BRISQUEScore, FramerateScore, ResolutionScore, GapsScore, TotalScore)

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
    close(fig)
