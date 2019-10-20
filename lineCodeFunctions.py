import numpy as np
import matplotlib.pyplot as plt
import random
from scipy.signal import butter, lfilter, freqz
# import bitarray

####################### Basic Functions #######################
random.seed(1)

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
    noise_sig = (lc + noise)*np.random.rayleigh(0.1)
    return noise_sig

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

def plotNoiseSig(noise,step,title,bits,save):
    fig, ax = plt.subplots(constrained_layout=True)
    ax.plot(noise)
    ax.set_xlabel('Time (ms)')
    ax.set_ylabel('Voltage (V)')
    ax.set_title(title+' signal with noise\nBits: '+ str(bits))

    def forward(noise):
        return noise*step

    def inverse(noise):
        return noise*step

    secax = ax.secondary_xaxis('top',functions=(forward, inverse))
    secax.set_xlabel('Bits')

    if save == True:
        fig.savefig("./images_noise/"+title+"_noise.png")
    # plt.show() 
    return 0

def pulseWaveform(step, bits, pulses,title):
    size = len(pulses)
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
    if plot == True and size <=32:        
        plotSignal(t, lc, bits, title)

    return lc

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

def filter(sig,order,fs,cutoff,step):
    b, a = butter_lowpass(cutoff, fs, order)

    plotSpec = False
    if plotSpec == True:
        # Plot the frequency response.
        w, h = freqz(b, a, worN=fs)
        plt.subplot(2, 1, 1)
        plt.plot(0.5*fs*w/np.pi, np.abs(h), 'b')
        plt.plot(cutoff, 0.5*np.sqrt(2), 'ko')
        plt.axvline(cutoff, color='k')
        plt.xlim(0, 0.1*fs)
        plt.title("Lowpass Filter Frequency Response")
        plt.xlabel('Frequency [Hz]')
        plt.grid()
        plt.show()

    y = butter_lowpass_filter(sig, cutoff, fs, order)

    return y

def plotPbSnr(pb,snr,title):
    fig = plt.figure()
    plt.subplot()
    plt.title(title)
    plt.plot(snr, pb)
    plt.xlabel('SNR (db)')
    plt.ylabel('Pb')
    plt.xscale('log')
    plt.grid(b=True, which='major', color='#444444', 
                        linestyle='-',alpha = 0.3)
    plt.minorticks_on()
    plt.grid(b=True, which='minor', color='#444444', 
                        linestyle='-',alpha = 0.2)
    fig.savefig("./images_noise/"+title+".png")
    # plt.show()
    
    return 0

def strToBits(text):
    # ba = bitarray.bitarray()
    # ba.frombytes(text.encode('utf-8'))
    # return ba

    bits = bin(int.from_bytes(text.encode(), 'big'))[2:]
    return list(map(int, bits.zfill(8 * ((len(bits) + 7) // 8))))

def bitsToStr(bits):
    # string = bitarray.bitarray(bits).tobytes().decode('utf-8')
    n = int(''.join(map(str, bits)), 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()

###################### Rate Calculations #######################

def rateBits(Ts,M):
    if M <= 2:                          # One bit for symbol 
        rate = 1/Ts
    else:           
        nBits = np.log2(M)              # N bits for symbol
        rate = (1/Ts)*nBits
    return rate

def rateError(y,y_noise,bits):   
    size_y = len(y_noise)
    size_bits = len(bits)
    step = int(size_y/size_bits)
    x = np.zeros(size_bits)
    x_noise = np.zeros(size_bits)
    z = np.zeros(size_bits)
    z_noise = np.zeros(size_bits)
    decoded = []
    L = 0   
    rate = 0
    wrong_bits = 0
    symbolIndex = 1
    shift = int(step/2) + 1

    for j in range(0, size_y):                      # Pega um valor com ruído no meio do bit, 
        if j == step*symbolIndex - shift:           # para armazenar cada bit enviado em um novo array com tamanho original
            x[symbolIndex-1] = y[step*symbolIndex-shift]
            x_noise[symbolIndex-1] = y_noise[step*symbolIndex-shift]
            symbolIndex = symbolIndex + 1

    for i in range(0,size_bits):
        if x[i] > L:
            z[i] = 1
        else:
            z[i] = -1
        
        if x_noise[i] > L:
            z_noise[i] = 1
            decoded.append(int(1))
        else:
            z_noise[i] = -1
            decoded.append(int(0))

        if z[i] != z_noise[i]:
            wrong_bits = wrong_bits + 1

    rate = (size_bits - wrong_bits)/size_bits
    pb =  wrong_bits/size_bits
    # print("Size: "+str(size_bits))
    # print("Wrong: "+str(wrong_bits))
    # print("Rate: "+str(rate))
    # print("Pb: "+str(pb))

    return pb,rate, decoded

############################ Line Codes ########################

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
    results = {}
    snr = 1
    cutoff = 160
    fs = 8000
    order = 6
    plot = False
    save_plot = False

    for j in range(0,n_iterations):                # Média de 10 vezes cada iteração de 45 valores de snr
        bits = bitsGen(n_bits)          # 1 vetor de bits para cada iteração (mesmo vetor para todos snr)
        bip_noise_res =[]
        bip_filt_res = []
        man_noise_res = []
        man_filt_res = []

        for i in range(0,45):
            print("\nSNR: "+str(snr))
            print("\n******** Bipolar ********")
            bipolarNRZ_lc = bipolarNRZ(bits, step) 
            bipolarNRZ_lc_noise = noiseGen(bipolarNRZ_lc,step,n_bits,snr)  
            bipolar_filtered = filter(bipolarNRZ_lc_noise,order,fs,cutoff,step)

            bipolar_rate_noise,x,y = rateError(bipolarNRZ_lc,bipolarNRZ_lc_noise,bits)
            bipolar_rate_filtered,x,y = rateError(bipolarNRZ_lc,bipolar_filtered,bits)


            print("\n******** Manchester ********") 
            manchester_lc = manchester(bits, step)
            manchester_lc_noise = noiseGen(manchester_lc,step,n_bits,snr)  
            manchester_filtered = filter(manchester_lc_noise,order,fs,cutoff,step)

            manc_rate_noise,x,y = rateError(manchester_lc,manchester_lc_noise,bits)
            manc_rate_filtered,x,y = rateError(manchester_lc,manchester_filtered,bits)

            bip_noise_res.append(bipolar_rate_noise)
            bip_filt_res.append(bipolar_rate_filtered)
            man_noise_res.append(manc_rate_noise)
            man_filt_res.append(manc_rate_filtered)

            snr = snr + 1

            if plot == True:
                plotNoiseSig(bipolarNRZ_lc_noise,step,"BipolarNRZ_6db_snr",bits,save_plot)
                plotNoiseSig(bipolar_filtered,step,"BipolarNRZ_filtered",bits,save_plot)
                plotNoiseSig(manchester_lc_noise,step,"Manchester_6db_snr",bits,save_plot)
                plotNoiseSig(manchester_filtered,step,"Manchester_filtered",bits,save_plot)

        data = { 
                    "BipolarNRZ_noise":bip_noise_res,
                    "BipolarNRZ_filtered":bip_filt_res,
                    "Manchester_noise":man_noise_res,
                    "Manchester_filtered":man_filt_res
        }

        results["Iteration_"+str(j)] = data
        snr = 1
        del bip_noise_res
        del bip_filt_res
        del man_noise_res
        del man_filt_res
        
    return results
