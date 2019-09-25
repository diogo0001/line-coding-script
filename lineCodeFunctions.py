import numpy as np
import matplotlib.pyplot as plt


def bitsGen(size):
    bits = np.random.randint(0, 2, size)
    return bits


def plotSignal(x, y,title):
    plt.step(x, y, where='post', label='post')
    plt.plot(x, y,'C0')
    plt.grid(True)
    plt.suptitle(title)
    plt.show()
    return 0


def pulseWaveform(step, size, Ts, pulses, plot,title):
    t = np.arange(0, size, step)
    size_t = len(t)
    xt = np.zeros(size_t)
    symbolIndex = 1
    # print(pulses)

    for j in range(0, size_t):
        if t[j] >= 0 and t[j] < symbolIndex:
            xt[j] = pulses[symbolIndex-1]
        else:
            xt[j] = pulses[symbolIndex]
            if symbolIndex < size-1:
                symbolIndex = symbolIndex+Ts

    if plot == True:
        plotSignal(t, xt,title)

    return xt

##### Line codings #####


def unipolarNRZ(bits, step, Ts, plot):
    size = len(bits)
    pulses = np.zeros(size)
    amp = 5
    for i in range(0, size):
        if bits[i] == 1:
            pulses[i] = amp
        else:
            pulses[i] = 0

    xt = pulseWaveform(step, size, Ts, pulses, plot,"Unipolar NRZ")
    return xt
