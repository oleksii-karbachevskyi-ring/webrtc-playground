Note: In order to run a scalable VP9 add following line to chromium's sender argument
```diff
        p_sender = sp.Popen(f'{_CHROMIUM_DIR}/src/out/Release/chrome \
        --use-fake-device-for-media-stream \
+       --force-fieldtrials=WebRTC-SupportVP9SVC/EnabledByFlag_2SL3TL
        --use-file-for-fake-video-capture={_FAKE_VIDEO_FILE} \
        --user-data-dir={_SENDER_USER_DATA_DIR} \
```
Run from `/scripts/` folder  
First run `collect.py`  
Then run `summary.py`  

Results are stored in `/script_results/vid-590/` folder

Main files are:
 - Total Score.png
 - BRISQUE Score.png
 - Framerate Score.png
 - Gaps Score.png
 - ResolutionScore.png