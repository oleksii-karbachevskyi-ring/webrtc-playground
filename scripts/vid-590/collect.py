from automate import Environment

# Loss influence
folder = '../script_results/vid-590'
for codec in ['H264', 'VP8', 'VP9']:
# for codec in ['VP9']:
    loss_to_suffix = {0:'000', 0.005:'005', 0.01:'010', 0.015:'015', 0.02:'020', 0.03:'030', 0.04: '040', 0.05:'050'}
    for loss in [0, 0.005, 0.01, 0.015, 0.02, 0.03, 0.04, 0.05]:
        env = Environment(80, 2000, loss=loss, codec=codec)
        env.run_test(20)
        env.cleanup()
        suffix = codec + loss_to_suffix[loss]
        # suffix = 'VP9-SVC' + loss_to_suffix[loss]
        print(suffix)
        env.save_output(f'{folder}/loss_{suffix}.ivf', f'{folder}/sender_{suffix}.log', f'{folder}/receiver_{suffix}.log')
