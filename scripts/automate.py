import subprocess as sp
import os
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep

_CHROMIUM_DIR           = '/home/oleksii/WS/chromium'
_WEBRTC_BACKEND_DIR     = '/home/oleksii/WS/webrtc-playground'
_UNIX_SOCKET            = _CHROMIUM_DIR + '/us'
_SENDER_USER_DATA_DIR   = '/home/oleksii/.config/chromium'
_RECEIVER_USER_DATA_DIR = '/home/oleksii/.config/chromium2'
_FAKE_VIDEO_FILE        = 'pedestrian_area_1080p25.y4m'

class Environment:
    def __init__(self, delay_ms=0, bandwidth_kbps=0, loss=0, http_port=8000, wss_port=8080, sender_cdp_port=5001, receiver_cdp_port=5002):
        self.__run_mahimahi(delay_ms, bandwidth_kbps, loss)
        # Tunnel's inner end
        self.p_shell.stdin.write(f'socat UNIX-LISTEN:{_UNIX_SOCKET},fork TCP4:localhost:5052 &\n')
        self.p_shell.stdin.flush()
        self.pid_in = 1
        # Tunnel's outter end
        self.p_out = sp.Popen(f'socat TCP-LISTEN:{receiver_cdp_port},fork,reuseaddr UNIX-CLIENT:{_UNIX_SOCKET}'.split(),
                              stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE, text=True)
        # HTTP and WebSocket Servers
        self.p_http = sp.Popen(f'python3 -m http.server {http_port}'.split(),
                              stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE, text=True, cwd=_WEBRTC_BACKEND_DIR)
        self.p_wss = sp.Popen(f'{_WEBRTC_BACKEND_DIR}/wsserver/Release/wsserver {wss_port}'.split(),
                              stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE, text=True)
        self.__run_receiver_chrome(receiver_cdp_port, http_port, wss_port)
        self.__run_sender_chrome(sender_cdp_port, http_port, wss_port)

    def run_test(self, duration):
        negotiateButton = self.sender_driver.find_element_by_id('negotiateButton')
        negotiateButton.click()

        sleep(duration)

    def cleanup(self):
        self.sender_driver.close()
        self.sender_driver.quit()
        self.sender_driver = None
        self.p_sender.communicate();

        self.receiver_driver.close()
        self.receiver_driver.quit()
        self.receiver_driver = None

        self.p_wss.terminate()
        self.p_wss.communicate()
        self.p_http.terminate()
        self.p_http.communicate()
        self.p_out.terminate()
        self.p_out.communicate()

        self.p_shell.stdin.write(f'kill -15 %{self.pid_in}\n')
        self.p_shell.stdin.flush()
        self.p_shell.communicate(input='exit\n')

    def save_output(self, ivf_file, sender_file, receiver_file):
        for e in os.listdir():
            if e.startswith('webrtc_receive_stream_'):
                st = os.stat(e)
                if st.st_size:
                    shutil.move(e, ivf_file)
                else:
                    os.remove(e)
        shutil.move('sender_log', sender_file)
        shutil.move('receiver_log', receiver_file)

    def __run_mahimahi(self, delay_ms, bandwidth_kbps, loss):
        delay_cmd = ''
        bandwidth_cmd = ''
        loss_cmd = ''
        if delay_ms:
            delay_cmd = 'mm-delay ' + str(delay_ms) + ' '
        if bandwidth_kbps:
            with open('up-limit-file', 'w') as f:
                f.write('1\n')
            # calculate interpacket delay for 1500 bytes packet
            inter_delay = int(12000/bandwidth_kbps + 0.5)
            with open('down-limit-file', 'w') as f:
                f.write(str(inter_delay) + '\n')
            bandwidth_cmd = 'mm-link up-limit-file down-limit-file '
        if loss:
            loss_cmd = 'mm-loss downlink ' + str(loss) + ' '
        mm_cmd = delay_cmd + bandwidth_cmd + loss_cmd
        if mm_cmd == '':
            mm_cmd = 'bash' # for reusing code
        self.p_shell = sp.Popen(mm_cmd.split(), stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE, text=True)
        self.p_shell.stdin.write('echo $MAHIMAHI_BASE\n')
        self.p_shell.stdin.flush()
        self.base = self.p_shell.stdout.readline().strip()

    def __run_sender_chrome(self, sender_cdp_port, http_port, wss_port):
        p_sender = sp.Popen(f'{_CHROMIUM_DIR}/src/out/Release/chrome \
        --use-fake-device-for-media-stream \
        --use-file-for-fake-video-capture={_FAKE_VIDEO_FILE} \
        --user-data-dir={_SENDER_USER_DATA_DIR} \
        --enable-automation \
        --remote-debugging-port={sender_cdp_port} \
        > sender_log 2>&1', stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE, text=True, shell=True)

        sender_options = Options()
        sender_options.debugger_address = f'127.0.0.1:{sender_cdp_port}'
        sender_driver = webdriver.Chrome(executable_path=f'{_CHROMIUM_DIR}/chromedriver', options=sender_options)
        sender_driver.get(f'http://127.0.0.1:{http_port}/content/sender/')
        
        server_elm = sender_driver.find_element_by_id('server')
        server_elm.clear(); server_elm.send_keys(f'127.0.0.1:{wss_port}')
        
        framerate_elm = sender_driver.find_element_by_id('framerate')
        framerate_elm.clear(); framerate_elm.send_keys('25')
        
        startButton = sender_driver.find_element_by_id('startButton')
        startButton.click()
        sleep(2)
        
        connectButton = sender_driver.find_element_by_id('connectButton')
        connectButton.click()
        self.p_sender = p_sender
        self.sender_driver = sender_driver

    def __run_receiver_chrome(self, receiver_cdp_port, http_port, wss_port):
        self.p_shell.stdin.write(f'{_CHROMIUM_DIR}/src/out/Release/chrome \
        --user-data-dir={_RECEIVER_USER_DATA_DIR} \
        --no-sandbox \
        --enable-automation \
        --remote-debugging-port=5052 \
        > receiver_log 2>&1 \n')
        self.p_shell.stdin.flush()

        receiver_options = Options()
        receiver_options.debugger_address = f'127.0.0.1:{receiver_cdp_port}'
        receiver_driver = webdriver.Chrome(executable_path=f'{_CHROMIUM_DIR}/chromedriver', options=receiver_options)
        
        receiver_driver.get(f'http://{self.base}:{http_port}/content/receiver/')
        rcv_server_elm = receiver_driver.find_element_by_id('server')
        rcv_server_elm.clear(); rcv_server_elm.send_keys(f'{self.base}:{wss_port}')
        rcv_connectButton = receiver_driver.find_element_by_id('connectButton')
        rcv_connectButton.click()
        sleep(1)
        self.receiver_driver = receiver_driver

## Usage
# env = Environment(30, 2000, 0.01)
# env.run_test(5)
# env.cleanup()
# env.save_output('script_results/file_1.ivf', 'script_results/sender_1.log', 'script_results/receiver_1.log')
# env = Environment(30, 2000, 0.02)
# env.run_test(5)
# env.cleanup()
# env.save_output('script_results/file_2.ivf', 'script_results/sender_2.log', 'script_results/receiver_2.log')
