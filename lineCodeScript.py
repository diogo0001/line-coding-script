import lineCodeFunctions as lc
import json

vectorSize = 16000                      # Tem que ser par
step = 0.01                             # Tempo de cada simbolo
n_iterations = 10                       # Para a média  

run_snr_iterations = False              # roda as iterações para os valores de snr e salva o json
open_json_mean_errors = False           # abre o json gerado e calcula as médias 
plot_SNRxPb = True
RESULTS_FILE = "Results.json"           # resultado bruto das iterações 
MEAN_ERRORS_FILE = "Results_mean.json"  # media dos resultados anteriores

run_text_message = False
text_test = "Hello! Lets check how many wrong characters will be received in this message"
MSG_ERRORS_FILE = "Msg_errors.json"

##############################################################

if run_snr_iterations == True:

    result = lc.rateErrorCalculatorScript(vectorSize,n_iterations,step)

    for x in result:
      print(result[x]["BipolarNRZ_noise"])

    result_json = json.dumps(result,indent=4)
    print(result_json)

    with open(RESULTS_FILE, "w") as write_file:
        json.dump(result, write_file,indent=4)

#############################################################

if open_json_mean_errors == True:
    with open(RESULTS_FILE,"r") as json_file:
        data = json.load(json_file)

    bip_noise_res =[]
    bip_filt_res = []
    man_noise_res = []
    man_filt_res = []
    mean = {}

    for i in data:                   # carrega os valores
        bip_noise_res.append(data[i]["BipolarNRZ_noise"])
        bip_filt_res.append(data[i]["BipolarNRZ_filtered"])
        man_noise_res.append(data[i]["Manchester_noise"])
        man_filt_res.append(data[i]["Manchester_filtered"])

    snr_size = len(bip_noise_res[0])
    pb_size = len(bip_noise_res)

    for j in range(0,snr_size):     # calcula as médias
        temp1 = []
        temp2 = []
        temp3 = []
        temp4 = []

        for i in range(0,pb_size):
            temp1.append(bip_noise_res[i][j])
            temp2.append(bip_filt_res[i][j])
            temp3.append(man_noise_res[i][j])
            temp4.append(man_filt_res[i][j])

        pb1 = sum(temp1) / float(len(temp1))
        pb2 = sum(temp2) / float(len(temp2))
        pb3 = sum(temp3) / float(len(temp3))
        pb4 = sum(temp4) / float(len(temp4))
        wb1 = int(pb1*vectorSize)
        wb2 = int(pb2*vectorSize)
        wb3 = int(pb3*vectorSize)
        wb4 = int(pb4*vectorSize)

        data = { 
                "BipolarNRZ_noise":{"Pb_mean":pb1,"Wrong_bits_mean":wb1},
                "BipolarNRZ_filtered":{"Pb_mean":pb2,"Wrong_bits_mean":wb2},
                "Manchester_noise":{"Pb_mean":pb3,"Wrong_bits_mean":wb3},
                "Manchester_filtered":{"Pb_mean":pb4,"Wrong_bits_mean":wb4}
            }

        mean["SNR_"+str(j)] = data

        del temp1 
        del temp2 
        del temp3 
        del temp4 
    
    temp1 = []
    temp2 = []
    temp3 = []
    temp4 = []
    snr = []
    j = 1
    for i in mean:
        temp1.append(mean[i]["BipolarNRZ_noise"]["Pb_mean"])
        temp2.append(mean[i]["BipolarNRZ_filtered"]["Pb_mean"])
        temp3.append(mean[i]["Manchester_noise"]["Pb_mean"])
        temp4.append(mean[i]["Manchester_filtered"]["Pb_mean"])
        snr.append(j)
        j = j + 1

    if plot_SNRxPb == True:
        title = "SRNxPb BipolarNRZ_noise "
        lc.plotPbSnr(temp1,snr,title)

        title = "SRNxPb BipolarNRZ_filtered "
        lc.plotPbSnr(temp2,snr,title)

        title = "SRNxPb Manchester_noise"
        lc.plotPbSnr(temp3,snr,title)

        title = "SRNxPb Manchester_filtered "
        lc.plotPbSnr(temp4,snr,title)


    with open(MEAN_ERRORS_FILE, "w") as write_file:
        json.dump(mean, write_file,indent=4)

#############################################################

def compare(x,y):
    size = len (x)
    wrong_bits = 0

    for i in range(0,size):
        if x[i] != y[i]:
            wrong_bits = wrong_bits + 1

    return wrong_bits

if run_text_message == True:
    bits = lc.strToBits(text_test)
    n_bits = len(bits)
    snr = 1
    iterations = 15
    errors = {}

    print(bits)

    for i in range(0,iterations):
        print("Bipolar")
        bipolarNRZ_lc = lc.bipolarNRZ(bits, step) 
        bipolarNRZ_lc_noise = lc.noiseGen(bipolarNRZ_lc,step,n_bits,snr)  
        bipolar_rate_noise,x,dec = lc.rateError(bipolarNRZ_lc,bipolarNRZ_lc_noise,bits)
        wrong_bip = compare(bits,dec) 
        print(wrong_bip)
        # msg_back = lc.bitsToStr(dec)
        # print(msg_back)

        print("Manchester")
        manchester_lc = lc.manchester(bits, step)
        manchester_lc_noise = lc.noiseGen(manchester_lc,step,n_bits,snr)  
        manc_rate_noise,x,dec = lc.rateError(manchester_lc,manchester_lc_noise,bits)
        wrong_man = compare(bits,dec) 
        print(wrong_man)
        # msg_back = lc.bitsToStr(dec)
        # print(msg_back)

        data = {
            "BipolarNRZ_error":wrong_bip,
            "Manchester_error":wrong_man
        }
        errors["SNR_"+str(snr)] = data
        snr = snr + 1

    with open(MSG_ERRORS_FILE, "w") as write_file:
        json.dump(errors, write_file,indent=4)

    print(errors)
    
