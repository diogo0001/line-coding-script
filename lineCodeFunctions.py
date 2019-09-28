import numpy as np
import matplotlib.pyplot as plt

####################### Basic Functions #######################

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
    plt.grid(b=True, which='major', color='#444444', 
                        linestyle='-',alpha = 0.3)
    plt.minorticks_on()
    plt.grid(b=True, which='minor', color='#444444', 
                        linestyle='-',alpha = 0.2)
    fig.savefig("./images/"+title+".png")
    # plt.show()
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
    if M <= 2:                          # Onde bit for symbol 
        rate = 1/Ts
    else:           
        nBits = np.log2(M)              # N bits for symbol
        rate = (1/Ts)*nBits
    return rate


def rateMean(pulses,bits,step,M):       # Modify to future tasks
    size = len(pulses)
    count = 0

    for i in range(0,size-1):
        if pulses[i] != pulses[i+1]:
            count = count + 1

    rate = count*step
    return rate


###################### Script Functions ######################## 

def bitsRate(n_bits,step,runBitsRate):
    results = np.zeros(shape=(9))
    bits = bitsGen(n_bits)
    m,results[0],y = unipolarNRZ(bits, step,False,runBitsRate) 
    m,results[1],y = unipolarRZ(bits, step, False,runBitsRate) 
    m,results[2],y = bipolarNRZ(bits, step, False,runBitsRate) 
    m,results[3],y = bipolarRZ(bits, step, False,runBitsRate) 
    m,results[4],y = NRZSpace(bits, step, False,runBitsRate) 
    m,results[5],y = manchester(bits, step, False,runBitsRate) 
    m,results[6],y = hdb3(bits, step, False,runBitsRate) 
    m,results[7],y = polarQuatNRZ(bits, step, False,runBitsRate) 
    m,results[8],y = twob1q(bits, step, False,runBitsRate)  
    return results

def rateCalculator(n_bits,n_iterations,step,runMean):
    results = np.zeros(shape=(9,n_iterations))

    for i in range(0,n_iterations):
        bits = bitsGen(n_bits)
        results[0][i],x,y = unipolarNRZ(bits, step,runMean,False) 
        results[1][i],x,y = unipolarRZ(bits, step, runMean,False) 
        results[2][i],x,y = bipolarNRZ(bits, step, runMean,False) 
        results[3][i],x,y = bipolarRZ(bits, step, runMean,False) 
        results[4][i],x,y = NRZSpace(bits, step, runMean,False) 
        results[5][i],x,y = manchester(bits, step, runMean,False) 
        results[6][i],x,y = hdb3(bits, step, runMean,False) 
        results[7][i],x,y = polarQuatNRZ(bits, step, runMean,False) 
        results[8][i],x,y = twob1q(bits, step, runMean,False)  
        # print(results)
    return results


############################ Line Codes #############################

def unipolarNRZ(bits, step,runMean,runBitRate):
    M = 2
    size = len(bits)
    pulses = np.zeros(size)
    amp = 5
    meanRate = 0
    bitRate = 0

    for i in range(0, size):
        if bits[i] == 1:
            pulses[i] = amp

    if runMean == True:
        meanRate = rateMean(pulses,bits,step,M)

    if runBitRate == True:
        bitRate = rateBits(step,M)

    lc = pulseWaveform(step, bits, pulses,"Unipolar NRZ")
    return meanRate, bitRate, lc

def unipolarRZ(bits, step,runMean,runBitRate):
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

    if runMean == True:
        meanRate = rateMean(pulses,bits,step,M)

    if runBitRate == True:
        bitRate = rateBits(step,M)

    lc = pulseWaveform(step, bits, pulses, "Unipolar RZ")
    return meanRate, bitRate, lc

def bipolarNRZ(bits, step, runMean,runBitRate):
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

    if runMean == True:
        meanRate = rateMean(pulses,bits,step,M)

    if runBitRate == True:
        bitRate = rateBits(step,M)

    lc = pulseWaveform(step, bits, pulses, "Bipolar NRZ")
    return meanRate, bitRate, lc

def bipolarRZ(bits, step, runMean,runBitRate):
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

    if runMean == True:
        meanRate = rateMean(pulses,bits,step,M)

    if runBitRate == True:
        bitRate = rateBits(step,M)

    lc = pulseWaveform(step, bits, pulses, "Bipolar RZ")
    return meanRate, bitRate, lc

def polarQuatNRZ(bits, step, runMean,runBitRate):
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
        
    if runMean == True:
        meanRate = rateMean(pulses,bits,step,M)

    if runBitRate == True:
        bitRate = rateBits(step,M)

    lc = pulseWaveform(step, bits, pulses, "Polar Quatern NRZ")
    return meanRate, bitRate, lc

def NRZSpace(bits, step, runMean,runBitRate):
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

    if runMean == True:
        meanRate = rateMean(pulses,bits,step,M)

    if runBitRate == True:
        bitRate = rateBits(step,M)

    lc = pulseWaveform(step, bits, pulses, "NRZ Space")
    return meanRate, bitRate, lc

def manchester(bits, step, runMean,runBitRate):
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

    if runMean == True:
        meanRate = rateMean(pulses,bits,step,M)

    if runBitRate == True:
        bitRate = rateBits(step,M)

    lc = pulseWaveform(step, bits, pulses, "Manchester")
    return meanRate, bitRate, lc

def hdb3(bits, step, runMean,runBitRate):
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

    if runMean == True:
        meanRate = rateMean(pulses,bits,step,M)

    if runBitRate == True:
        bitRate = rateBits(step,M)

    lc = pulseWaveform(step, bits, pulses, "HDB3")
    return meanRate, bitRate, lc

def twob1q(bits, step, runMean,runBitRate):  
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

    if runMean == True:
        meanRate = rateMean(pulses,bits,step,M)   

    if runBitRate == True:
        bitRate = rateBits(step,M)
        
    lc = pulseWaveform(step, bits, pulses, "2B1Q")
    return meanRate, bitRate, lc
