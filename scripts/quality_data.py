import pandas as pd
from log_data import ProcessTwoLogs

def ProcessByCommonName(common):
    sender_logname = 'results/sender_' + common + '_log'
    receiver_logname = 'results/receiver_' + common + '_log'
    return ProcessTwoLogs(sender_logname, receiver_logname)

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
    data_300_000_000 = ProcessByCommonName('300_000_000')
    data_300_000_050 = ProcessByCommonName('300_000_050')
    data_300_000_200 = ProcessByCommonName('300_000_200')
    data_300_005_000 = ProcessByCommonName('300_005_000')
    data_300_005_050 = ProcessByCommonName('300_005_050')
    data_300_005_200 = ProcessByCommonName('300_005_200')
    data_300_020_000 = ProcessByCommonName('300_020_000')
    data_300_020_050 = ProcessByCommonName('300_020_050')
    data_300_020_200 = ProcessByCommonName('300_020_200')
    data_800_000_000 = ProcessByCommonName('800_000_000')
    data_800_000_050 = ProcessByCommonName('800_000_050')
    data_800_000_200 = ProcessByCommonName('800_000_200')
    data_800_005_000 = ProcessByCommonName('800_005_000')
    data_800_005_050 = ProcessByCommonName('800_005_050')
    data_800_005_200 = ProcessByCommonName('800_005_200')
    data_800_020_000 = ProcessByCommonName('800_020_000')
    data_800_020_050 = ProcessByCommonName('800_020_050')
    data_800_020_200 = ProcessByCommonName('800_020_200')
    data_1500_000_000 = ProcessByCommonName('1500_000_000')
    data_1500_000_050 = ProcessByCommonName('1500_000_050')
    data_1500_000_200 = ProcessByCommonName('1500_000_200')
    data_1500_005_000 = ProcessByCommonName('1500_005_000')
    data_1500_005_050 = ProcessByCommonName('1500_005_050')
    data_1500_005_200 = ProcessByCommonName('1500_005_200')
    data_1500_020_000 = ProcessByCommonName('1500_020_000')
    data_1500_020_050 = ProcessByCommonName('1500_020_050')
    data_1500_020_200 = ProcessByCommonName('1500_020_200')
    data_2000_000_000 = ProcessByCommonName('2000_000_000')
    data_2000_000_050 = ProcessByCommonName('2000_000_050')
    data_2000_000_200 = ProcessByCommonName('2000_000_200')
    data_2000_005_000 = ProcessByCommonName('2000_005_000')
    data_2000_005_050 = ProcessByCommonName('2000_005_050')
    data_2000_005_200 = ProcessByCommonName('2000_005_200')
    data_2000_020_000 = ProcessByCommonName('2000_020_000')
    data_2000_020_050 = ProcessByCommonName('2000_020_050')
    data_2000_020_200 = ProcessByCommonName('2000_020_200')

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
