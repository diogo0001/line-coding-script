import lineCodeFunctions as lc
import json
import numpy as np

vectorSize = 32  # must be pair
step = 0.01
n_iterations = 10

fileName = "Results.json"
saveFile = open("Results.txt","w")



def rateCalculator(n_bits,n_iterations,step,f):
    results = np.zeros(shape=(9,n_iterations))

    for i in range(0,n_iterations):
        bits = lc.bitsGen(n_bits)
        # x, unipolarNRZ= lc.unipolarNRZ(bits, step, True,True) 
        # x, unipolarRZ = lc.unipolarRZ(bits, step, True,True) 
        # x, bipolarNRZ = lc.bipolarNRZ(bits, step, True,True) 
        # x, bipolarRZ = lc.bipolarRZ(bits, step, True,True) 
        # x, NRZSpace = lc.NRZSpace(bits, step, True,True) 
        # x, manchester = lc.manchester(bits, step, True,True) 
        # x, hdb3 = lc.hdb3(bits, step,  True,True) 
        # x, polarQuatNRZ = lc.polarQuatNRZ(bits, step, True,True) 
        # x, twob1q = lc.twob1q(bits, step, True,True)  
        # results.append( [unipolarNRZ, unipolarRZ, bipolarNRZ, bipolarRZ, NRZSpace, manchester, hdb3, polarQuatNRZ, twob1q])

        results[0][i],x = lc.unipolarNRZ(bits, step, True,True) 
        results[1][i],x = lc.unipolarRZ(bits, step, True,True) 
        results[2][i],x = lc.bipolarNRZ(bits, step, True,True) 
        results[3][i],x = lc.bipolarRZ(bits, step, True,True) 
        results[4][i],x = lc.NRZSpace(bits, step, True,True) 
        results[5][i],x = lc.manchester(bits, step, True,True) 
        results[6][i],x = lc.hdb3(bits, step, True,True) 
        results[7][i],x = lc.polarQuatNRZ(bits, step, True,True) 
        results[8][i],x = lc.twob1q(bits, step, True,True)  

        print(results)

    # data = {
    #     str(n_bits)+"_bits":{
    #         "unipolarNRZ":results[0],
    #         "unipolarRZ":results[1],
    #         "bipolarNRZ":results[2],
    #         "bipolarRZ":results[3],
    #         "NRZSpace":results[4],
    #         "manchester":results[5],
    #         "hdb3":results[6],
    #         "polarQuatNRZ":results[7],
    #         "twob1q":results[8]
    #     }
    # }
    # with open(fileName, 'w') as f:
    #     json.dump(data, f)
    return results

############### Calculations ###################

vectorSize = 32
result = rateCalculator(vectorSize,n_iterations,step,saveFile)
saveFile.write("Results for "+str(vectorSize)+" bits:\n\n")
saveFile.write(str(result))

vectorSize = 1024
result = rateCalculator(vectorSize,n_iterations,step,saveFile)
saveFile.write("\n\n\nResults for "+str(vectorSize)+" bits:\n\n")
saveFile.write(str(result))


vectorSize = 8192
result = rateCalculator(vectorSize,n_iterations,step,saveFile)
saveFile.write("\n\n\nResults for "+str(vectorSize)+" bits:\n\n")
saveFile.write(str(result))

vectorSize = 16384
result = rateCalculator(vectorSize,n_iterations,step,saveFile)
saveFile.write("\n\n\nResults for "+str(vectorSize)+" bits:\n\n")
saveFile.write(str(result))