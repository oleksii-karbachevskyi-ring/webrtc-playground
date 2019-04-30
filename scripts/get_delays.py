# Run me from ~/WS/chromium
import re
import csv
import pandas as pd
# from matplotlib.pyplot import plot, stackplot
from matplotlib.pyplot import figure, close

class FrameInfo:
    FrameType = None
    FrameSize = None
    CaptureTime = None
    TS1 = None
    TS2 = None
    EncStart = None
    EncStop = None
    PayEnd = None
    PacerEnd = None
    ReceiveStart = None
    ReceiveStop = None
    t1 = None
    t2 = None

class FrameAnalyzer:
    def __init__(self):
        self._packets = []

    def OnEncodeLine(self, line):
        # [1:3:0326/110709.861347:WARNING:video_stream_encoder.cc(1094)] TIME_ENC 3 23979 87023891 4096153392
        p =  r'\[\d*:\d*:\d*/(\d\d)(\d\d)(\d\d)\.(\d*).*TIME_ENC (\d*) (\d*) (\d*) (\d*)'
        m = re.match(p, line)
        if (m == None):
            print('Wrong line:' + line)
            return
        lexems = m.groups()
        t = 3600.0*float(lexems[0]) + 60.0*float(lexems[1]) + float(lexems[2]) + float(lexems[3])/1e6
        self.OnEncodeInfo(int(lexems[4]), int(lexems[5]), int(lexems[6]), int(lexems[7]), t)

    def OnDecodeLine(self, line):
        # [1:17:0326/110709.989404:WARNING:video_receive_stream.cc(434)] TIME_DEC 3 23979 1904476641 12 172 173 298 87024071 87024192
        p =  r'\[\d*:\d*:\d*/(\d\d)(\d\d)(\d\d)\.(\d*).*TIME_DEC (\d*) (\d*) (\d*) (-?\d*) (\d*) (\d*) (\d*) (\d*) (\d*)'
        m = re.match(p, line)
        if (m == None):
            print('Wrong line:' + line)
            return
        lexems = m.groups()
        t = 3600.0*float(lexems[0]) + 60.0*float(lexems[1]) + float(lexems[2]) + float(lexems[3])/1e6
        self.OnDecodeInfo(int(lexems[4]), int(lexems[5]), int(lexems[6]), int(lexems[7]), int(lexems[8]), int(lexems[9]), int(lexems[10]), int(lexems[11]), int(lexems[12]), t)

    def OnEncodeInfo(self, FrameType, FrameSize, CaptureTime, TS1, t):
        # FrameType FrameSize CaptureTime        TS1
        #         3     23979    87023891 4096153392
        fi = FrameInfo()
        fi.FrameType = FrameType
        fi.FrameSize = FrameSize
        fi.CaptureTime = CaptureTime
        fi.TS1 = TS1
        fi.t1 = t
        self._packets.append(fi)

    def OnDecodeInfo(self, FrameType, FrameSize, TS2, EncStart, EncStop, PayEnd, PacerEnd, ReceiveStart, ReceiveStop, t):
        # FrameType FrameSize        TS2 EncStart EncStop PayEnd PacerEnd ReceiveStart ReceiveStop
        #         3     23979 1904476641       12     172    173      298     87024071    87024192
        cont = True
        ind = len(self._packets) - 1
        while cont:
            if self._packets[ind].FrameSize == FrameSize:
                cont = False
                self._packets[ind].TS2 = TS2
                self._packets[ind].EncStart = EncStart
                self._packets[ind].EncStop = EncStop
                self._packets[ind].PayEnd = PayEnd
                self._packets[ind].PacerEnd = PacerEnd
                self._packets[ind].ReceiveStart = ReceiveStart
                self._packets[ind].ReceiveStop = ReceiveStop
                self._packets[ind].t2 = t
            elif ind == 0 or t - self._packets[ind].t1 > 30.0:
                cont = False
            ind -= 1

    def PrintInfo(self, path):
        f = open(path, 'w')
        w = csv.writer(f)
        w.writerow(['Frame Id', 'Frame Size', 'Received', 'Capture Time', 'Total Delay', 'Encoding Delay', 'Network Delay'])
        ind = 0
        for p in self._packets:
            Received = 'N'
            CaptureTime = p.CaptureTime
            TotalDelay = None
            EncodingDelay = None
            NetworkDelay = None
            if p.t2:
                Received = 'Y'
                TotalDelay = p.ReceiveStop - p.CaptureTime
                EncodingDelay = p.EncStop - p.EncStart
                NetworkDelay = TotalDelay - EncodingDelay
            w.writerow([ind, p.FrameSize, Received, CaptureTime, TotalDelay, EncodingDelay, NetworkDelay])
            ind += 1

def PlotData(title, csv_file, png_name):
    frame = pd.read_csv(csv_file)
    fig = figure(figsize=(12, 8))
    ax = fig.add_subplot(111)
    t = (frame['Capture Time'] - min(frame['Capture Time']))/1000.0
    ax.stackplot(t, frame['Encoding Delay'], frame['Network Delay'], labels=['Encoding Delay', 'Network Delay'])
    ax.set_title(title)
    ax.set_xlabel('Time, s')
    ax.set_ylabel('Delay, ms')
    ax.legend()
    ax.set_xlim(0, 30)
    ax.set_ylim(0, 1000)
    fig.savefig(png_name)

def ProcessLog(logname, title, csv_file, png_name):
    f = open('src/out/Release/' + logname)
    fa = FrameAnalyzer()
    for l in f.readlines():
        if 'TIME_ENC' in l:
            fa.OnEncodeLine(l)
        elif 'TIME_DEC' in l:
            fa.OnDecodeLine(l)
        else:
            pass
    fa.PrintInfo(csv_file)
    PlotData(title, csv_file, png_name)

def ProcessTwoLogs(sender_logname, receiver_logname, title, csv_file, png_name):
    f_s = open('src/out/Release/' + sender_logname)
    f_r = open('src/out/Release/' + receiver_logname)
    d = []
    for l in f_s.readlines():
        if 'TIME_ENC' in l:
            l = re.sub(r'\d*:\d*', '1:1', l, count=1)
            d.append(l)
    for l in f_r.readlines():
        if 'TIME_DEC' in l:
            l = re.sub(r'\d*:\d*', '1:1', l, count=1)
            d.append(l)
    d.sort()
    fa = FrameAnalyzer()
    for l in d:
        if 'TIME_ENC' in l:
            fa.OnEncodeLine(l)
        elif 'TIME_DEC' in l:
            fa.OnDecodeLine(l)
        else:
            pass
    fa.PrintInfo(csv_file)
    PlotData(title, csv_file, png_name)

ProcessTwoLogs('sender_log', 'receiver_log', '100 ms + 5% loss', '100ms_0.05.csv', '100ms_0.05.png')
# ProcessLog('h264_log', 'H.264', 'h264.csv', 'h264.png')

close('all')