import numpy as np
import matplotlib.pyplot as plt
import random

####################### Basic Functions #######################
random.seed(1)

def gen():
    return np.random.rayleigh(0.5)

def bitsGen(size):
    bits = np.random.randint(0, 2, size)
    return bits

def getSnrNoise(snr,sig):
    watts = sig**2
    sigDb = 10 * np.log10(watts)

    sig_avg_watts = np.mean(watts)
    sig_avg_db = 10 * np.log10(sig_avg_watts)

    noise_avg_db = sig_avg_db - snr
    noise_avg_watts = 10 ** (noise_avg_db / 20)
    # print(noise_avg_watts)
    return noise_avg_watts 

def noiseGen(lc,step,n_bits,snr): 
    coef = getSnrNoise(snr,lc)
    noise = np.random.normal(0,coef,len(lc))
    noise = (lc + noise)*np.random.rayleigh(0.4)
    return noise

def plotSignal(x,y,bits,title):
    fig = plt.figure()
    plt.subplot()
    plt.title(title+" - "+str(bits))
    plt.plot(x, y)
    plt.xlabel('Time (ms)')
    plt.ylabel('Voltage (V)')
    plt.grid(b=True, which='major', color='#444444', 
                        linestyle='-',alpha = 0.3)
    plt.minorticks_on()
    plt.grid(b=True, which='minor', color='#444444', 
                        linestyle='-',alpha = 0.2)
    fig.savefig("./images/"+title+".png")
    # plt.show()
    return 0

def plotNoiseSig(noise,step,title):
    fig, ax = plt.subplots(constrained_layout=True)
    ax.plot(noise)
    ax.set_xlabel('Time (ms)')
    ax.set_ylabel('Voltage (V)')
    ax.set_title(title+' signal with noise')

    def forward(noise):
        return noise*step

    def inverse(noise):
        return noise*step

    secax = ax.secondary_xaxis('top',functions=(forward, inverse))
    secax.set_xlabel('Bits')
    # fig.savefig("./images_noise/"+title+"_noise.png")
    plt.show() 
    
    return 0

def pulseWaveform(step, bits, pulses,title):
    size = len(pulses)
    sizeBits = len(bits)
    t = np.arange(0, size, step)
    size_t = len(t)
    lc = np.zeros(size_t)
    symbolIndex = 1

    for j in range(0, size_t):
        if t[j] >= 0 and t[j] < symbolIndex:
            lc[j] = pulses[symbolIndex-1]
        else:
            lc[j] = pulses[symbolIndex]
            if symbolIndex < size-1:
                symbolIndex = symbolIndex+1
                
    plot = False
    if plot == True and sizeBits <=32:        
        plotSignal(t, lc, bits, title)

    return lc

###################### Rate Calculations #######################

def rateBits(Ts,M):
    if M <= 2:                          # One bit for symbol 
        rate = 1/Ts
    else:           
        nBits = np.log2(M)              # N bits for symbol
        rate = (1/Ts)*nBits
    return rate

def rateError(y,y_noise,bits):      
    rate = 0
    size = len(y_noise)
    L = 0
    z = np.zeros(size)
    zn = np.zeros(size)
    zero = np.zeros(size)

    for i in range(0,size):
        if y_noise[i] > L:
            zn[i] = 1
        else:
            zn[i] = -1
        
        if y[i] > L:
            z[i] = 1
        else:
            z[i] = -1

    dif = z-zn
    rate = list(set(dif) - set(zero))
    print(len(rate))
    return rate
        
###################### Script Functions ######################## 

def bitsRateScript(n_bits,step,runBitsRate):
    results = np.zeros(shape=(9))
    results[0] = rateBits(step,2) 
    results[1] = rateBits(step,2)
    results[2] = rateBits(step,2)
    results[3] = rateBits(step,2)
    results[4] = rateBits(step,2)
    results[5] = rateBits(step,2)
    results[6] = rateBits(step,2)
    results[7] = rateBits(step,4)
    results[8] = rateBits(step,4)

    plot = False
    if plot == True:
        names = ['uni-NRZ', 'uni-RZ', 'bi-NRZ','bi-RZ', 'NRZ-S', 'manchest','hdb3', 'pol4-NRZ', '2b1q']
        plt.rcdefaults()
        fig, ax = plt.subplots()
        y_pos = np.arange(len(names))
        error = np.random.rand(len(names))
        ax.barh(y_pos, results, xerr=error, align='center')
        ax.set_yticks(y_pos)
        ax.set_yticklabels(names)
        ax.invert_yaxis()  # labels read top-to-bottom
        ax.set_xlabel('Taxa de bits')
        ax.set_title('Taxa de bits por codificação com Ts: '+str(step)+'s')
        fig.savefig("./images/bitsRate.png")
        # plt.show()
    return results

def rateErrorCalculatorScript(n_bits,n_iterations,step):
    results = np.zeros(shape=(4,n_iterations))
    snr = 5

    for i in range(0,n_iterations):
        bits = bitsGen(n_bits)
        # print(bits)
        bipolarNRZ_lc = bipolarNRZ(bits, step) 
        bipolarNRZ_lc_noise = noiseGen(bipolarNRZ_lc,step,n_bits,snr)  
        meanRate_bipolar = rateError(bipolarNRZ_lc,bipolarNRZ_lc_noise,bits)


        # NRZSpace_lc = NRZSpace(bits, step) 
        # NRZSpace_lc_noise = noiseGen(NRZSpace_lc,step,snr)  
        # meanRate_NRZ = rateError(NRZSpace_lc,NRZSpace_lc_noise)

        # manchester_lc = manchester(bits, step)
        # manchester_lc_noise = noiseGen(manchester_lc,step,snr)  
        # meanRate_man = rateError(manchester_lc,manchester_lc_noise) 

    return results

############################ Line Codes #############################

def unipolarNRZ(bits, step):
    M = 2
    size = len(bits)
    pulses = np.zeros(size)
    amp = 5
    meanRate = 0
    bitRate = 0

    for i in range(0, size):
        if bits[i] == 1:
            pulses[i] = amp

    lc = pulseWaveform(step, bits, pulses,"Unipolar NRZ")
    return lc

def unipolarRZ(bits, step):
    M = 2
    size = len(bits)
    pulses = np.zeros(size*2)
    amp = 5
    j = 0
    meanRate = 0
    bitRate = 0

    for i in range(0, size):
        if bits[i] == 1:
            pulses[j] = amp
            pulses[j+1] = 0
        
        j = j + 2

    lc = pulseWaveform(step, bits, pulses, "Unipolar RZ")
    return  lc

def bipolarNRZ(bits, step):
    M = 2
    size = len(bits)
    pulses = np.zeros(size)
    amp = 5
    meanRate = 0
    bitRate = 0
    for i in range(0, size):
        if bits[i] == 1:
            pulses[i] = amp
        else:
            pulses[i] = -amp

    title = "Bipolar NRZ"
    lc = pulseWaveform(step, bits, pulses,title)
    return  lc

def bipolarRZ(bits, step):
    M = 2
    size = len(bits)
    pulses = np.zeros(size*2)
    amp = 5
    j = 0
    meanRate = 0
    bitRate = 0

    for i in range(0, size):
        if bits[i] == 1:
            pulses[j] = amp
            pulses[j+1] = 0
        else:
            pulses[j] = -amp
            pulses[j+1] = 0
        j = j + 2

    lc = pulseWaveform(step, bits, pulses, "Bipolar RZ")
    return  lc

def polarQuatNRZ(bits, step):
    M = 4
    size = int(len(bits)/2)
    pulses = np.zeros(size)
    amp = 3.5
    j = 0
    meanRate = 0
    bitRate = 0

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
        
    lc = pulseWaveform(step, bits, pulses, "Polar Quatern NRZ")
    return meanRate, bitRate, lc

def NRZSpace(bits, step):
    M = 2
    size = len(bits)
    pulses = np.zeros(size)
    amp = 5
    meanRate = 0
    bitRate = 0

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

    title = "NRZ Space"
    lc = pulseWaveform(step, bits, pulses,title)
    return lc

def manchester(bits, step):
    M = 2
    size = len(bits)
    pulses = np.zeros(size*2)
    amp = 5
    j = 0
    meanRate = 0
    bitRate = 0

    for i in range(0,size):
        if bits[i] == 1:
            pulses[j] = amp
            pulses[j+1] = -amp
        else:
            pulses[j] = -amp
            pulses[j+1] = amp
        j = j + 2

    title = "Manchester"
    lc = pulseWaveform(step, bits, pulses,title)
    return lc

def hdb3(bits, step):
    M = 2
    size = len(bits)
    ami = np.zeros(size)
    V = np.zeros(size)
    B = np.zeros(size)
    amp = 5
    oneFlag = True
    zeroCount = 0
    sign = 0
    meanRate = 0
    bitRate = 0

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

    lc = pulseWaveform(step, bits, pulses, "HDB3")
    return  lc

def twob1q(bits, step):  
    M = 4
    size = int(len(bits)/2)
    pulses = np.zeros(size)
    amp = 2.5
    j = 0
    meanRate = 0
    bitRate = 0

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
  
    lc = pulseWaveform(step, bits, pulses, "2B1Q")
    return lc
