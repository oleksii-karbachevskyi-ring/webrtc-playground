import os
import shelve
import shutil as sh
import subprocess as sp
import numpy as np
import concurrent.futures
import multiprocessing

def GetResolutionAndFramerate(video_file):
    output = sp.run(['ffprobe', video_file], capture_output=True).stderr.decode().split('\n')
    for line in output:
        if 'Video' in line:
            # Stream #0:0: Video: h264 (Constrained Baseline) (H264 / 0x34363248), yuv420p(progressive), 1920x1080, 25 tbr, 90k tbn, 180k tbc
            lexems = line.split(',')
            if len(lexems) != 6:
                return (0,0,0)
            w, h = lexems[2][1:].split('x') # 1920x1080,
            fps = lexems[3][1:].split(' ')[0]
            return int(w), int(h), float(fps)
    return (0,0,0)

def CalcBRISQUE(video_file, regenerate = False):
    s = shelve.open('brisque')
    res = []
    if regenerate or not video_file in s:
        tmp_dir = '2i1ohi'
        sh.rmtree(tmp_dir, ignore_errors=True)
        os.mkdir(tmp_dir)
        sp.run(['ffmpeg', '-i', video_file, tmp_dir + '/%d.png'], capture_output=True)
        all_ok = True
        fno = 1
        wd = '/home/oleksii/Downloads/release1.3/bin'
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=multiprocessing.cpu_count())
        def task(wd, path):
            output = sp.run([wd + '/brisquequality', path], capture_output=True, cwd=wd).stdout.decode()
            return float(output.split()[2])
        while all_ok:
            fpath = tmp_dir + '/' + str(fno) + '.png'
            if os.path.isfile(fpath):
                res.append(executor.submit(task, wd,os.getcwd() + '/' + fpath))
            else:
                all_ok = False
            fno += 10
        for i in range(len(res)):
            res[i] = res[i].result()
        executor.shutdown()
        sh.rmtree(tmp_dir)
        s[video_file] = res
    else:
        res = s[video_file]
    s.close()
    return res

def GetBRISQUEScore(video_file, regenerate = False):
    bris_scores = CalcBRISQUE(video_file, regenerate)
    return 30.0 * (1.0 - np.average(bris_scores)/100.0)

def GetGapsScoreFromCaptureTimes(capture_times_ms):
    max_score = 40 # points
    subscore_left_point  = 10000 # 10 seconds
    subscore_right_point = 20000 # 20 seconds
    score_penalty = 10 # points
    duration_param = 8000 # 8 seconds
    total_duration = capture_times_ms[-1] - capture_times_ms[0]
    if total_duration == 0:
        return max_score
    total_gap_duration = 0
    gaps = []
    prev = capture_times_ms[0]
    for i in range(1, len(capture_times_ms)):
        curr = capture_times_ms[i]
        if curr - prev > 200:
            total_gap_duration += curr - prev
            gaps.append(curr - prev)
        prev = curr
    if total_gap_duration <= subscore_left_point:
        subscore = max_score
    elif total_gap_duration <= subscore_right_point:
        subscore = max_score - (total_gap_duration - subscore_left_point)/(subscore_right_point - subscore_left_point)*score_penalty
    else:
        subscore = max_score - score_penalty
    gaps.sort()
    n_gaps = min(len(gaps), 5)
    if n_gaps == 0:
        return subscore
    gaps = gaps[-n_gaps:]
    ave_gap = sum(gaps)/n_gaps
    if ave_gap > duration_param:
        return 0
    return (1.0 - ave_gap/duration_param)*subscore

def GetResolutionScore(w, h):
    if w*h <= 640*360:
        return 0.0
    elif w*h <= 848*480:
        return 6.0
    elif w*h <= 1280*720:
        return 14.0
    elif w*h <= 1920*1080:
        return 20.0
    else:
        return 20.0

def GetFramerateScore(fps):
    if fps <= 7.5:
        return 0.0
    elif fps <= 15.0:
        return 3.0
    elif fps <= 20.0:
        return 7.0
    elif fps <= 25.0:
        return 10.0
    else:
        return 10.0

def GetScore(video_file, capture_times_ms):
    w, h, fps = GetResolutionAndFramerate(video_file)
    return GetBRISQUEScore(video_file) + GetGapsScoreFromCaptureTimes(capture_times_ms) + GetResolutionScore(w, h) + GetFramerateScore(fps)

if __name__ == '__main__':
    CalcBRISQUE('/home/oleksii/WS/chromium/results/300_000_000.ivf')
    # GetResolutionAndFramerate('/home/oleksii/WS/chromium/results/300_000_000.ivf')
    print(GetScore('/home/oleksii/WS/chromium/results/300_000_000.ivf', [
            13300214.0, 13300611.0, 13301575.0, 13302132.0, 13302449.0, 13302695.0, 13302974.0, 13303214.0, 13303485.0, 13304325.0,
            13304685.0, 13304964.0, 13305284.0, 13305884.0, 13306245.0, 13306446.0, 13306605.0, 13306846.0, 13307045.0, 13307404.0,
            13307725.0, 13308005.0, 13308284.0, 13308606.0, 13308845.0, 13309125.0, 13309486.0, 13310006.0, 13310765.0, 13311444.0,
            13311804.0, 13311965.0, 13312165.0, 13312365.0, 13312563.0, 13312804.0, 13313163.0, 13313684.0, 13314084.0, 13314444.0,
            13314724.0, 13315324.0, 13315764.0, 13316205.0, 13316565.0, 13316924.0, 13317245.0, 13317565.0, 13317806.0, 13318044.0,
            13318324.0, 13318403.0]))
    pass