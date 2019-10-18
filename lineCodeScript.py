import lineCodeFunctions as lc
import json

vectorSize = 16000                      # Tem que ser par
step = 0.01                             # Tempo de cada simbolo
n_iterations = 10                       # Para a média  

run_snr_iterations = False              # roda as iterações para os valores de snr e salva o json
open_json_mean_errors = False           # abre o json gerado e calcula as médias 
RESULTS_FILE = "Results.json"           # resultado bruto das iterações 
MEAN_ERRORS_FILE = "Results_mean.json"  # media dos resultados anteriores

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

    for i in data:
        bip_noise_res.append(data[i]["BipolarNRZ_noise"])
        bip_filt_res.append(data[i]["BipolarNRZ_filtered"])
        man_noise_res.append(data[i]["Manchester_noise"])
        man_filt_res.append(data[i]["Manchester_filtered"])

    for j in range(0,len(bip_noise_res[0])):
        temp1 = []
        temp2 = []
        temp3 = []
        temp4 = []

        for i in range(0,len(bip_noise_res)):
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
        
    with open(MEAN_ERRORS_FILE, "w") as write_file:
        json.dump(mean, write_file,indent=4)

#############################################################

