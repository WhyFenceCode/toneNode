from pyo import *

s = Server(audio="portaudio", buffersize=8192).boot()
s.start()

#AUDIO CODE GOES HERE ==============



#AUDIO CODE STOP HERE ==============

input("Press Enter to stop...")
s.stop()
s.shutdown()