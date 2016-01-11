import sys
import wave
import struct
from scipy import signal
import numpy as np
from itertools import chain
from numpy import *
from scipy import *

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
    time = float(framesNumber) / frameRate
    data = data * signal.nuttall(framesNumber)
    dataFFT = fft(data)
    absFFT = abs(dataFFT)
    logAbsFFT = np.log(absFFT)
    hps = copy(logAbsFFT)
    for h in np.arange(2, 6):
        decim = signal.decimate(logAbsFFT, int(h))
        hps[:len(decim)] += decim
    start = 150
    peak = np.argmax(hps[start::])
    fundamental = ((start+peak)/time)
    return fundamental

def decision():
    fileName = sys.argv[1]
    data, channels, sampwidth, frameRate, framesNumber = readWaveFile(fileName)
    freq = getFreq(data, framesNumber, frameRate)
    if freq>170:
        print ('K')
    else:
        print ('M')

if __name__ == '__main__':
    decision()