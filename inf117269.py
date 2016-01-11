import sys
import wave
import struct
from scipy import signal
import numpy as np
from itertools import chain
from copy import copy

def readWaveFile(fileName):
    waveFile = wave.open(fileName,'r')
    channels = waveFile.getnchannels()
    sampWidth = waveFile.getsampwidth()
    framesNumber = waveFile.getnframes()
    frameRate = waveFile.getframerate()
    frames = waveFile.readframes(framesNumber)
    data = struct.unpack("%dh" %  channels*framesNumber, frames)
    oneChannelData = data[::channels]
    oneChannelData = list(chain(oneChannelData))
    framesNumber = len(oneChannelData)
    waveFile.close()
    return oneChannelData, channels, sampWidth, frameRate, framesNumber

def getFreq(data,framesNumber,frameRate):
    duration = float(framesNumber) / frameRate
    data = data * signal.nuttall(framesNumber)
    spectrum = np.log(abs(np.fft.rfft(data)))
    hps = copy(spectrum)
    for h in np.arange(2, 6):
        dec = signal.decimate(spectrum, int(h))
        hps[:len(dec)] += dec
    peak_start = 50 * duration
    peak = np.argmax(hps[peak_start:])
    fundamental = (peak_start + peak) / duration
    return fundamental

def decision():
    fileName = sys.argv[1]
    data, channels, sampwidth, frameRate, framesNumber = readWaveFile(fileName)
    freq = getFreq(data, framesNumber, frameRate)
    # print (freq)
    if freq>170:
        print ('K')
    else:
        print ('M')

if __name__ == '__main__':
    decision()