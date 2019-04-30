import re
import numpy as np
import pandas as pd

class FrameAnalyzer:
    def __init__(self):
        self._packets = pd.DataFrame(columns=['FrameType', 'FrameSize', 'CaptureTime', 'TS1', 'TS2', 'EncStart', 'EncStop', 'PayEnd', 'PacerEnd', 'ReceiveStart',
                                              'ReceiveStop', 't1', 't2'])
        # self._packets = self._packets.astype(np.int64)
        # self._packets['t1'] = self._packets['t1'].astype(np.float64)
        # self._packets['t2'] = self._packets['t2'].astype(np.float64)

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
        self._packets = self._packets.append(dict(FrameType=FrameType, FrameSize=FrameSize, CaptureTime=CaptureTime, TS1=TS1, t1=t), ignore_index=True)

    def OnDecodeInfo(self, FrameType, FrameSize, TS2, EncStart, EncStop, PayEnd, PacerEnd, ReceiveStart, ReceiveStop, t):
        # FrameType FrameSize        TS2 EncStart EncStop PayEnd PacerEnd ReceiveStart ReceiveStop
        #         3     23979 1904476641       12     172    173      298     87024071    87024192
        cont = True
        ind = len(self._packets) - 1
        while cont:
            if self._packets.iloc[ind].FrameSize == FrameSize:
                cont = False
                self._packets.iloc[ind].TS2 = TS2
                self._packets.iloc[ind].EncStart = EncStart
                self._packets.iloc[ind].EncStop = EncStop
                self._packets.iloc[ind].PayEnd = PayEnd
                self._packets.iloc[ind].PacerEnd = PacerEnd
                self._packets.iloc[ind].ReceiveStart = ReceiveStart
                self._packets.iloc[ind].ReceiveStop = ReceiveStop
                self._packets.iloc[ind].t2 = t
            elif ind == 0 or t - self._packets.iloc[ind].t1 > 30.0:
                cont = False
            ind -= 1

    def GetData(self):
        return self._packets

def ProcessTwoLogs(common):
    sender_logname = 'results/sender_' + common + '_log'
    receiver_logname = 'results/receiver_' + common + '_log'
    f_s = open(sender_logname)
    f_r = open(receiver_logname)
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
    return fa.GetData()

def GetDataFromLogs():
    global data_300_000_000
    global data_300_000_050
    global data_300_000_200
    global data_300_005_000
    global data_300_005_050
    global data_300_005_200
    global data_300_020_000
    global data_300_020_050
    global data_300_020_200
    global data_800_000_000
    global data_800_000_050
    global data_800_000_200
    global data_800_005_000
    global data_800_005_050
    global data_800_005_200
    global data_800_020_000
    global data_800_020_050
    global data_800_020_200
    global data_1500_000_000
    global data_1500_000_050
    global data_1500_000_200
    global data_1500_005_000
    global data_1500_005_050
    global data_1500_005_200
    global data_1500_020_000
    global data_1500_020_050
    global data_1500_020_200
    global data_2000_000_000
    global data_2000_000_050
    global data_2000_000_200
    global data_2000_005_000
    global data_2000_005_050
    global data_2000_005_200
    global data_2000_020_000
    global data_2000_020_050
    global data_2000_020_200
    data_300_000_000 = ProcessTwoLogs('300_000_000')
    data_300_000_050 = ProcessTwoLogs('300_000_050')
    data_300_000_200 = ProcessTwoLogs('300_000_200')
    data_300_005_000 = ProcessTwoLogs('300_005_000')
    data_300_005_050 = ProcessTwoLogs('300_005_050')
    data_300_005_200 = ProcessTwoLogs('300_005_200')
    data_300_020_000 = ProcessTwoLogs('300_020_000')
    data_300_020_050 = ProcessTwoLogs('300_020_050')
    data_300_020_200 = ProcessTwoLogs('300_020_200')
    data_800_000_000 = ProcessTwoLogs('800_000_000')
    data_800_000_050 = ProcessTwoLogs('800_000_050')
    data_800_000_200 = ProcessTwoLogs('800_000_200')
    data_800_005_000 = ProcessTwoLogs('800_005_000')
    data_800_005_050 = ProcessTwoLogs('800_005_050')
    data_800_005_200 = ProcessTwoLogs('800_005_200')
    data_800_020_000 = ProcessTwoLogs('800_020_000')
    data_800_020_050 = ProcessTwoLogs('800_020_050')
    data_800_020_200 = ProcessTwoLogs('800_020_200')
    data_1500_000_000 = ProcessTwoLogs('1500_000_000')
    data_1500_000_050 = ProcessTwoLogs('1500_000_050')
    data_1500_000_200 = ProcessTwoLogs('1500_000_200')
    data_1500_005_000 = ProcessTwoLogs('1500_005_000')
    data_1500_005_050 = ProcessTwoLogs('1500_005_050')
    data_1500_005_200 = ProcessTwoLogs('1500_005_200')
    data_1500_020_000 = ProcessTwoLogs('1500_020_000')
    data_1500_020_050 = ProcessTwoLogs('1500_020_050')
    data_1500_020_200 = ProcessTwoLogs('1500_020_200')
    data_2000_000_000 = ProcessTwoLogs('2000_000_000')
    data_2000_000_050 = ProcessTwoLogs('2000_000_050')
    data_2000_000_200 = ProcessTwoLogs('2000_000_200')
    data_2000_005_000 = ProcessTwoLogs('2000_005_000')
    data_2000_005_050 = ProcessTwoLogs('2000_005_050')
    data_2000_005_200 = ProcessTwoLogs('2000_005_200')
    data_2000_020_000 = ProcessTwoLogs('2000_020_000')
    data_2000_020_050 = ProcessTwoLogs('2000_020_050')
    data_2000_020_200 = ProcessTwoLogs('2000_020_200')

def SaveDataToCSV():
    data_300_000_000.to_csv('300_000_000.csv')
    data_300_000_050.to_csv('300_000_050.csv')
    data_300_000_200.to_csv('300_000_200.csv')
    data_300_005_000.to_csv('300_005_000.csv')
    data_300_005_050.to_csv('300_005_050.csv')
    data_300_005_200.to_csv('300_005_200.csv')
    data_300_020_000.to_csv('300_020_000.csv')
    data_300_020_050.to_csv('300_020_050.csv')
    data_300_020_200.to_csv('300_020_200.csv')
    data_800_000_000.to_csv('800_000_000.csv')
    data_800_000_050.to_csv('800_000_050.csv')
    data_800_000_200.to_csv('800_000_200.csv')
    data_800_005_000.to_csv('800_005_000.csv')
    data_800_005_050.to_csv('800_005_050.csv')
    data_800_005_200.to_csv('800_005_200.csv')
    data_800_020_000.to_csv('800_020_000.csv')
    data_800_020_050.to_csv('800_020_050.csv')
    data_800_020_200.to_csv('800_020_200.csv')
    data_1500_000_000.to_csv('1500_000_000.csv')
    data_1500_000_050.to_csv('1500_000_050.csv')
    data_1500_000_200.to_csv('1500_000_200.csv')
    data_1500_005_000.to_csv('1500_005_000.csv')
    data_1500_005_050.to_csv('1500_005_050.csv')
    data_1500_005_200.to_csv('1500_005_200.csv')
    data_1500_020_000.to_csv('1500_020_000.csv')
    data_1500_020_050.to_csv('1500_020_050.csv')
    data_1500_020_200.to_csv('1500_020_200.csv')
    data_2000_000_000.to_csv('2000_000_000.csv')
    data_2000_000_050.to_csv('2000_000_050.csv')
    data_2000_000_200.to_csv('2000_000_200.csv')
    data_2000_005_000.to_csv('2000_005_000.csv')
    data_2000_005_050.to_csv('2000_005_050.csv')
    data_2000_005_200.to_csv('2000_005_200.csv')
    data_2000_020_000.to_csv('2000_020_000.csv')
    data_2000_020_050.to_csv('2000_020_050.csv')
    data_2000_020_200.to_csv('2000_020_200.csv')

def LoadDataFromCSV():
    global data_300_000_000
    global data_300_000_050
    global data_300_000_200
    global data_300_005_000
    global data_300_005_050
    global data_300_005_200
    global data_300_020_000
    global data_300_020_050
    global data_300_020_200
    global data_800_000_000
    global data_800_000_050
    global data_800_000_200
    global data_800_005_000
    global data_800_005_050
    global data_800_005_200
    global data_800_020_000
    global data_800_020_050
    global data_800_020_200
    global data_1500_000_000
    global data_1500_000_050
    global data_1500_000_200
    global data_1500_005_000
    global data_1500_005_050
    global data_1500_005_200
    global data_1500_020_000
    global data_1500_020_050
    global data_1500_020_200
    global data_2000_000_000
    global data_2000_000_050
    global data_2000_000_200
    global data_2000_005_000
    global data_2000_005_050
    global data_2000_005_200
    global data_2000_020_000
    global data_2000_020_050
    global data_2000_020_200
    data_300_000_000 = pd.read_csv('300_000_000.csv')
    data_300_000_050 = pd.read_csv('300_000_050.csv')
    data_300_000_200 = pd.read_csv('300_000_200.csv')
    data_300_005_000 = pd.read_csv('300_005_000.csv')
    data_300_005_050 = pd.read_csv('300_005_050.csv')
    data_300_005_200 = pd.read_csv('300_005_200.csv')
    data_300_020_000 = pd.read_csv('300_020_000.csv')
    data_300_020_050 = pd.read_csv('300_020_050.csv')
    data_300_020_200 = pd.read_csv('300_020_200.csv')
    data_800_000_000 = pd.read_csv('800_000_000.csv')
    data_800_000_050 = pd.read_csv('800_000_050.csv')
    data_800_000_200 = pd.read_csv('800_000_200.csv')
    data_800_005_000 = pd.read_csv('800_005_000.csv')
    data_800_005_050 = pd.read_csv('800_005_050.csv')
    data_800_005_200 = pd.read_csv('800_005_200.csv')
    data_800_020_000 = pd.read_csv('800_020_000.csv')
    data_800_020_050 = pd.read_csv('800_020_050.csv')
    data_800_020_200 = pd.read_csv('800_020_200.csv')
    data_1500_000_000 = pd.read_csv('1500_000_000.csv')
    data_1500_000_050 = pd.read_csv('1500_000_050.csv')
    data_1500_000_200 = pd.read_csv('1500_000_200.csv')
    data_1500_005_000 = pd.read_csv('1500_005_000.csv')
    data_1500_005_050 = pd.read_csv('1500_005_050.csv')
    data_1500_005_200 = pd.read_csv('1500_005_200.csv')
    data_1500_020_000 = pd.read_csv('1500_020_000.csv')
    data_1500_020_050 = pd.read_csv('1500_020_050.csv')
    data_1500_020_200 = pd.read_csv('1500_020_200.csv')
    data_2000_000_000 = pd.read_csv('2000_000_000.csv')
    data_2000_000_050 = pd.read_csv('2000_000_050.csv')
    data_2000_000_200 = pd.read_csv('2000_000_200.csv')
    data_2000_005_000 = pd.read_csv('2000_005_000.csv')
    data_2000_005_050 = pd.read_csv('2000_005_050.csv')
    data_2000_005_200 = pd.read_csv('2000_005_200.csv')
    data_2000_020_000 = pd.read_csv('2000_020_000.csv')
    data_2000_020_050 = pd.read_csv('2000_020_050.csv')
    data_2000_020_200 = pd.read_csv('2000_020_200.csv')

def FillMaps():
    bitrate_data_300_000 = {'000':data_300_000_000, '050':data_300_000_050, '200':data_300_000_200}
    bitrate_data_300_005 = {'000':data_300_005_000, '050':data_300_005_050, '200':data_300_005_200}
    bitrate_data_300_020 = {'000':data_300_020_000, '050':data_300_020_050, '200':data_300_020_200}
    bitrate_data_800_000 = {'000':data_800_000_000, '050':data_800_000_050, '200':data_800_000_200}
    bitrate_data_800_005 = {'000':data_800_005_000, '050':data_800_005_050, '200':data_800_005_200}
    bitrate_data_800_020 = {'000':data_800_020_000, '050':data_800_020_050, '200':data_800_020_200}
    bitrate_data_1500_000 = {'000':data_1500_000_000, '050':data_1500_000_050, '200':data_1500_000_200}
    bitrate_data_1500_005 = {'000':data_1500_005_000, '050':data_1500_005_050, '200':data_1500_005_200}
    bitrate_data_1500_020 = {'000':data_1500_020_000, '050':data_1500_020_050, '200':data_1500_020_200}
    bitrate_data_2000_000 = {'000':data_2000_000_000, '050':data_2000_000_050, '200':data_2000_000_200}
    bitrate_data_2000_005 = {'000':data_2000_005_000, '050':data_2000_005_050, '200':data_2000_005_200}
    bitrate_data_2000_020 = {'000':data_2000_020_000, '050':data_2000_020_050, '200':data_2000_020_200}
    global bitrate_data_300
    global bitrate_data_800
    global bitrate_data_1500
    global bitrate_data_2000
    bitrate_data_300  = {'000':bitrate_data_300_000,  '005':bitrate_data_300_005,  '020':bitrate_data_300_020}
    bitrate_data_800  = {'000':bitrate_data_800_000,  '005':bitrate_data_800_005,  '020':bitrate_data_800_020}
    bitrate_data_1500 = {'000':bitrate_data_1500_000, '005':bitrate_data_1500_005, '020':bitrate_data_1500_020}
    bitrate_data_2000 = {'000':bitrate_data_2000_000, '005':bitrate_data_2000_005, '020':bitrate_data_2000_020}

    delay_data_000_300  = {'000':data_300_000_000,  '005':data_300_005_000,  '020':data_300_020_000}
    delay_data_000_800  = {'000':data_800_000_000,  '005':data_800_005_000,  '020':data_800_020_000}
    delay_data_000_1500 = {'000':data_1500_000_000, '005':data_1500_005_000, '020':data_1500_020_000}
    delay_data_000_2000 = {'000':data_2000_000_000, '005':data_2000_005_000, '020':data_2000_020_000}

    delay_data_050_300  = {'000':data_300_000_050,  '005':data_300_005_050,  '020':data_300_020_050}
    delay_data_050_800  = {'000':data_800_000_050,  '005':data_800_005_050,  '020':data_800_020_050}
    delay_data_050_1500 = {'000':data_1500_000_050, '005':data_1500_005_050, '020':data_1500_020_050}
    delay_data_050_2000 = {'000':data_2000_000_050, '005':data_2000_005_050, '020':data_2000_020_050}

    delay_data_200_300  = {'000':data_300_000_200,  '005':data_300_005_200,  '020':data_300_020_200}
    delay_data_200_800  = {'000':data_800_000_200,  '005':data_800_005_200,  '020':data_800_020_200}
    delay_data_200_1500 = {'000':data_1500_000_200, '005':data_1500_005_200, '020':data_1500_020_200}
    delay_data_200_2000 = {'000':data_2000_000_200, '005':data_2000_005_200, '020':data_2000_020_200}

    global delay_data_000
    global delay_data_050
    global delay_data_200
    delay_data_000 = {'300':delay_data_000_300, '800':delay_data_000_800, '1500':delay_data_000_1500, '2000':delay_data_000_2000}
    delay_data_050 = {'300':delay_data_050_300, '800':delay_data_050_800, '1500':delay_data_050_1500, '2000':delay_data_050_2000}
    delay_data_200 = {'300':delay_data_200_300, '800':delay_data_200_800, '1500':delay_data_200_1500, '2000':delay_data_200_2000}
    # delay_data_delay_bitrate_loss

def GetData(regenerate = False):
    if regenerate:
        GetDataFromLogs()
        SaveDataToCSV()
    else:
        LoadDataFromCSV()
    FillMaps()
    return (bitrate_data_300, bitrate_data_800, bitrate_data_1500, bitrate_data_2000, delay_data_000, delay_data_050, delay_data_200)
