import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)


def bitsGen(size):
    bits = np.random.randint(0, 2, size)
    return bits


def plotSignal(x,y,bits,title):
    fig = plt.figure()
    plt.subplot()
    plt.title(title+" - "+str(bits))
    plt.plot(x, y)
    plt.xlabel('Time (ms)')
    plt.ylabel('Voltage (V)')
    plt.grid(b=True, which='major', color='#444444', linestyle='-',alpha = 0.3)
    plt.minorticks_on()
    plt.grid(b=True, which='minor', color='#444444', linestyle='-',alpha = 0.2)
    fig.savefig("./images/"+title+".png")
    # plt.show()
    return 0


def pulseWaveform(step, bits, Ts, pulses, plot,title):
    size = len(pulses)
    sizeBits = len(bits)

    if sizeBits*2 == size: 
        t = np.arange(0, size, step/2)
    else:
        t = np.arange(0, size, step)

    size_t = len(t)
    lc = np.zeros(size_t)
    symbolIndex = 1
    # print(pulses)

    for j in range(0, size_t):
        if t[j] >= 0 and t[j] < symbolIndex:
            lc[j] = pulses[symbolIndex-1]
        else:
            lc[j] = pulses[symbolIndex]
            if symbolIndex < size-1:
                symbolIndex = symbolIndex+Ts
                
    # plot = False
    if plot == True and sizeBits <=32:          # plot if less or 32 bits
        plotSignal(t, lc, bits, title)

    return lc

############################ Line codings #############################


def unipolarNRZ(bits, step, Ts, plot):
    size = len(bits)
    pulses = np.zeros(size)
    amp = 5
    for i in range(0, size):
        if bits[i] == 1:
            pulses[i] = amp
        else:
            pulses[i] = 0

    lc = pulseWaveform(step, bits, Ts, pulses, plot,"Unipolar NRZ")
    return lc


def unipolarRZ(bits, step, Ts, plot):
    size = len(bits)
    pulses = np.zeros(size*2)
    amp = 5
    j = 0

    for i in range(0, size):
        if bits[i] == 1:
            pulses[j] = amp
            pulses[j+1] = 0
        else:
            pulses[j] = 0
            pulses[j+1] = 0
        j = j + 2

    lc = pulseWaveform(step, bits, Ts, pulses, plot,"Unipolar RZ")
    return lc


def bipolarNRZ(bits, step, Ts, plot):
    size = len(bits)
    pulses = np.zeros(size)
    amp = 5
    for i in range(0, size):
        if bits[i] == 1:
            pulses[i] = amp
        else:
            pulses[i] = -amp

    lc = pulseWaveform(step, bits, Ts, pulses, plot,"Bipolar NRZ")
    return lc


def bipolarRZ(bits, step, Ts, plot):
    size = len(bits)
    pulses = np.zeros(size*2)
    amp = 5
    j = 0

    for i in range(0, size):
        if bits[i] == 1:
            pulses[j] = amp
            pulses[j+1] = 0
        else:
            pulses[j] = -amp
            pulses[j+1] = 0
        j = j + 2

    lc = pulseWaveform(step, bits, Ts, pulses, plot,"Bipolar RZ")
    return lc


def polarQuatNRZ(bits, step, Ts, plot):
    size = int(len(bits)/2)
    pulses = np.zeros(size)
    amp = 3.5
    j = 0

    for i in range(0, len(bits),2):
        if i%2 == 0:
            if bits[i] == 0 and bits[i+1] == 0:
                pulses[j] = -3*amp/2
            elif bits[i] == 0 and bits[i+1] == 1:
                pulses[j] = -amp/2
            elif bits[i] == 1 and bits[i+1] == 0:
                pulses[j] = amp/2
            elif bits[i] == 1 and bits[i+1] == 1:
                pulses[j] = 3*amp/2
        j = j + 1
        
    lc = pulseWaveform(step, bits, Ts, pulses, plot,"Polar Quatern NRZ")
    return lc 


def NRZSpace(bits, step, Ts, plot):
    size = len(bits)
    pulses = np.zeros(size)
    amp = 5

    for i in range(0, size-1):
        if  bits[i] != bits[i+1] :
            pulses[i+1] = not pulses[i]
        elif bits[i] == 0 and bits[i+1]==0:
            pulses[i+1] = not pulses[i]
        else:
            pulses[i+1] = pulses[i]

    for i in range(0, size):
        if pulses[i] == 1:
            pulses[i] = amp
        else:
            pulses[i] = 0

    lc = pulseWaveform(step, bits, Ts, pulses, plot,"NRZ Space")
    return lc 


def manchester(bits, step, Ts, plot):
    size = len(bits)
    pulses = np.zeros(size*2)
    amp = 5
    j = 0

    for i in range(0,size):

        if bits[i] == 1:
            pulses[j] = amp
            pulses[j+1] = -amp
        else:
            pulses[j] = -amp
            pulses[j+1] = amp
        j = j + 2


    lc = pulseWaveform(step, bits, Ts, pulses, plot,"Manchester")
    return lc 


def hdb3(bits, step, Ts, plot):
    size = len(bits)
    ami = np.zeros(size)
    V = np.zeros(size)
    B = np.zeros(size)
    amp = 5
    oneFlag = True
    zeroCount = 0
    sign = 0

    for i in range(0, size):            # AMI code for ones
        if bits[i] == 1:
            if oneFlag == True:
                ami[i] = amp
            else:
                ami[i] = -amp
            oneFlag = not oneFlag

    pulses = ami

    for i in range(0, size):
        if ami[i] == 0 :
            zeroCount = zeroCount + 1
            if zeroCount == 4:
                zeroCount = 0
                pulses[i] = pulses[i-4]
                V[i] = pulses[i]
                if pulses[i] == sign:
                    pulses[i] = -pulses[i]
                    pulses[i-3] = pulses[i]
                    B[i-3] = pulses[i]
                    V[i] = pulses[i]
                    pulses[i+1:size] = -pulses[i+1:size]
                sign = pulses[i]
        else:
            zeroCount = 0

    lc = pulseWaveform(step, bits, Ts, pulses, plot,"HDB3")
    return lc            


def twob1q(bits, step, Ts, plot):  
    size = int(len(bits)/2)
    pulses = np.zeros(size)
    amp = 2.5
    j = 0

    for i in range(0, len(bits),2):
        if i%2 == 0:
            if bits[i] == 0 and bits[i+1] == 0:
                pulses[j] = -amp
            elif bits[i] == 0 and bits[i+1] == 1:
                pulses[j] = -amp/3
            elif bits[i] == 1 and bits[i+1] == 1:
                pulses[j] = amp/3
            elif bits[i] == 1 and bits[i+1] == 0:
                pulses[j] = amp
        j = j + 1
        
    lc = pulseWaveform(step, bits, Ts, pulses, plot,"2B1Q")
    return lc 