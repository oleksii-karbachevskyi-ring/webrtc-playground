# Run me from ~/WS/chromium
import numpy as np
import pandas as pd
from matplotlib.pyplot import figure, close
import quality_data as qd
import objective_quality as oq

def AddBitratePlot(ax, d, label):
    captureTime = np.array(d.CaptureTime)
    captureTime -= np.min(captureTime)
    frameSize = np.array(d.FrameSize)[:-1]
    durations = (captureTime[1:] - captureTime[:-1])/1000.0 # seconds
    ax.plot(captureTime[:-1]/1000.0, 8*frameSize/durations/1000, '-', label=label)

def AddDelayPlot(ax, d, label):
    captureTime = np.array(d.CaptureTime)
    captureTime -= np.min(captureTime)
    delay = d.ReceiveStop - d.CaptureTime
    ax.plot(captureTime/1000.0, delay, '-', label=label)

def DrawBitrate(data, title, png_name = None):
    fig = figure(figsize=(12, 8))
    ax = fig.add_subplot(111)
    AddBitratePlot(ax,data['000']['000'], 'loss = 0.0 %, delay = 0 ms')
    AddBitratePlot(ax,data['000']['050'], 'loss = 0.0 %, delay = 50 ms')
    AddBitratePlot(ax,data['000']['200'], 'loss = 0.0 %, delay = 200 ms')
    AddBitratePlot(ax,data['005']['000'], 'loss = 0.5 %, delay = 0 ms')
    AddBitratePlot(ax,data['005']['050'], 'loss = 0.5 %, delay = 50 ms')
    AddBitratePlot(ax,data['005']['200'], 'loss = 0.5 %, delay = 200 ms')
    AddBitratePlot(ax,data['020']['000'], 'loss = 2.0 %, delay = 0 ms')
    AddBitratePlot(ax,data['020']['050'], 'loss = 2.0 %, delay = 50 ms')
    AddBitratePlot(ax,data['020']['200'], 'loss = 2.0 %, delay = 200 ms')
    ax.legend()
    ax.set_ylim(bottom=0)
    ax.set_xlim(left=0)
    ax.set_xlabel('Time, s')
    ax.set_ylabel('Bitrate, kbps')
    ax.set_title(title)
    fig.tight_layout()
    if png_name:
        fig.savefig(png_name)

def DrawDelay(data, title, png_name = None):
    fig = figure(figsize=(12, 8))
    ax = fig.add_subplot(111)
    AddDelayPlot(ax,data['300']['000'], 'bitrate = 300 kbps, loss = 0.0 %')
    AddDelayPlot(ax,data['300']['005'], 'bitrate = 300 kbps, loss = 0.5 %')
    AddDelayPlot(ax,data['300']['020'], 'bitrate = 300 kbps, loss = 2.0 %')
    AddDelayPlot(ax,data['800']['000'], 'bitrate = 800 kbps, loss = 0.0 %')
    AddDelayPlot(ax,data['800']['005'], 'bitrate = 800 kbps, loss = 0.5 %')
    AddDelayPlot(ax,data['800']['020'], 'bitrate = 800 kbps, loss = 2.0 %')
    AddDelayPlot(ax,data['1500']['000'], 'bitrate = 1500 kbps, loss = 0.0 %')
    AddDelayPlot(ax,data['1500']['005'], 'bitrate = 1500 kbps, loss = 0.5 %')
    AddDelayPlot(ax,data['1500']['020'], 'bitrate = 1500 kbps, loss = 2.0 %')
    AddDelayPlot(ax,data['2000']['000'], 'bitrate = 2000 kbps, loss = 0.0 %')
    AddDelayPlot(ax,data['2000']['005'], 'bitrate = 2000 kbps, loss = 0.5 %')
    AddDelayPlot(ax,data['2000']['020'], 'bitrate = 2000 kbps, loss = 2.0 %')
    ax.legend()
    ax.set_ylim(bottom=0)
    ax.set_xlim(left=0)
    ax.set_xlabel('Time, s')
    ax.set_ylabel('Delay, ms')
    ax.set_title(title)
    fig.tight_layout()
    if png_name:
        fig.savefig(png_name)

def GetScore(ivf_file, data):
    capture_times_ms = data.CaptureTime[pd.notna(data.TS2)].tolist()
    return oq.GetScore(ivf_file, capture_times_ms)

def DrawQuality(data, ivf_prefix, title, png_name = None):
    fig = figure(figsize=(12, 8))
    ax = fig.add_subplot(111)
    labels = []
    values = []
    labels.append('loss = 0.0 %, delay = 0 ms'  ); values.append(GetScore(ivf_prefix + '000_000.ivf', data['000']['000']))
    labels.append('loss = 0.0 %, delay = 50 ms' ); values.append(GetScore(ivf_prefix + '000_050.ivf', data['000']['050']))
    labels.append('loss = 0.0 %, delay = 200 ms'); values.append(GetScore(ivf_prefix + '000_200.ivf', data['000']['200']))
    labels.append('loss = 0.5 %, delay = 0 ms'  ); values.append(GetScore(ivf_prefix + '005_000.ivf', data['005']['000']))
    labels.append('loss = 0.5 %, delay = 50 ms' ); values.append(GetScore(ivf_prefix + '005_050.ivf', data['005']['050']))
    labels.append('loss = 0.5 %, delay = 200 ms'); values.append(GetScore(ivf_prefix + '005_200.ivf', data['005']['200']))
    labels.append('loss = 2.0 %, delay = 0 ms'  ); values.append(GetScore(ivf_prefix + '020_000.ivf', data['020']['000']))
    labels.append('loss = 2.0 %, delay = 50 ms' ); values.append(GetScore(ivf_prefix + '020_050.ivf', data['020']['050']))
    labels.append('loss = 2.0 %, delay = 200 ms'); values.append(GetScore(ivf_prefix + '020_200.ivf', data['020']['200']))
    ax.barh(range(9,0,-1), values, tick_label=labels)
    ax.set_xlim(left=60, right=80)
    ax.set_xlabel('Quality score')
    ax.set_title(title)
    fig.tight_layout()
    if png_name:
        fig.savefig(png_name)

def Test1():
    DrawBitrate(bitrate_data_300, '300 kbps', 'Bitrate 300.png')
    DrawBitrate(bitrate_data_800, '800 kbps', 'Bitrate 800.png')
    DrawBitrate(bitrate_data_1500, '1500 kbps', 'Bitrate 1500.png')
    DrawBitrate(bitrate_data_2000, '2000 kbps', 'Bitrate 2000.png')

def Test2():
    DrawDelay(delay_data_000, 'mm-delay 0 ms', 'Delay 0.png')
    DrawDelay(delay_data_050, 'mm-delay 50 ms', 'Delay 50.png')
    DrawDelay(delay_data_200, 'mm-delay 200 ms', 'Delay 200.png')

def Test3():
    DrawQuality(bitrate_data_300,  'results/300_',   '300 kbps', 'Quality 300.png')
    DrawQuality(bitrate_data_800,  'results/800_',   '800 kbps', 'Quality 800.png')
    DrawQuality(bitrate_data_1500, 'results/1500_', '1500 kbps', 'Quality 1500.png')
    DrawQuality(bitrate_data_2000, 'results/2000_', '2000 kbps', 'Quality 2000.png')

def Test4():
    data = bitrate_data_1500['020']['200']
    video_file = 'results/1500_020_200.ivf'
    capture_times_ms = np.array(data.CaptureTime[pd.notna(data.TS2)].tolist())
    inter_frame_deltas = capture_times_ms[1:] - capture_times_ms[:-1]
    fig = figure(figsize=(12, 8))
    ax = fig.add_subplot(111)
    ax.plot(inter_frame_deltas, '.')
    ax.set_xlabel('Frame #')
    ax.set_ylabel('Interframe delay, ms')
    ax.set_title('1500 kbps, 2.0 loss, 200 ms delay')
    w, h, fps = oq.GetResolutionAndFramerate(video_file)
    BRISQUEScore = oq.GetBRISQUEScore(video_file)
    FramerateScore = oq.GetFramerateScore(fps)
    ResolutionScore = oq.GetResolutionScore(w, h)
    GapsScore = oq.GetGapsScoreFromCaptureTimes(capture_times_ms)
    TotalScore = BRISQUEScore + FramerateScore + ResolutionScore + GapsScore
    print(f'Width = {w}')
    print(f'Height = {h}')
    print(f'Framerate = {fps}')
    print(f'BRISQUEScore = {BRISQUEScore}')
    print(f'FramerateScore = {FramerateScore}')
    print(f'ResolutionScore = {ResolutionScore}')
    print(f'GapsScore = {GapsScore}')
    print(f'TotalScore = {TotalScore}')

bitrate_data_300, bitrate_data_800, bitrate_data_1500, bitrate_data_2000, delay_data_000, delay_data_050, delay_data_200 = qd.GetData(regenerate = False)
# Test1()
# Test2()
Test3()
# Test4()
