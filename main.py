from pyo import *

s = Server(audio="portaudio", buffersize=1024).boot()
s.start()

# ================= TIMING & SEQUENCER =================
bpm = 125
beat_time = 60.0 / bpm 

met = Metro(time=beat_time, poly=1).play()
pattern_iter = Iter(met, choice=[1, 0, 0, 1, 1, 0])
seq_trig = met * pattern_iter

# ================= KICK SOUND DESIGN =================
pit_env = TrigLinseg(seq_trig, list=[(0, 0), (0.001, 1), (0.02, 0.8), (0.025, 0)], mul=80, add=30)
amp_env = TrigLinseg(seq_trig, list=[(0, 0), (0.005, 1), (0.25, 0)], mul=1)
osc = Sine(freq=pit_env, mul=amp_env)
click_env = TrigLinseg(seq_trig, list=[(0, 1), (0.01, 0)], mul=0.2)
click_noise = Noise(mul=click_env)
kick_source = osc + click_noise
hp_filt = Biquad(kick_source, freq=30, q=0.7, type=2)
kick_distorted = Disto(hp_filt, drive=1.0, slope=0.9, mul=0.8)
kick_processed = Compress(
    kick_distorted,   # input
    -12,              # threshold
    4,                # ratio
    0.005,            # attack_time (5ms)
    0.1,              # release_time (100ms)
    mul=1
)
kick_processed.out()

# ================= KEEP ALIVE =================
print("Playing... Press Enter to stop.")
try:
    input()
except:
    pass

s.stop()
s.shutdown()