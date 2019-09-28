import lineCodeFunctions as lc

# Necessary values to line code functions
vectorSize = 32  # Must be pair
step = 0.01      # Time for each symbol

# To run the bits rate (vector size can be small, 4 bits)
runBitsRate = True


# To run the mean rate
runMean = False
runAll = False
n_iterations = 10
saveFile = open("Results_mean.txt","w")


##################### Bits Rate Calculations ####################

results = lc.bitsRate(4,step,runBitsRate)
print(results)

##################### Rate Mean Calculations ####################

if  runMean:
    vectorSize = 32
    result = lc.rateCalculator(vectorSize,n_iterations,step,runMean)
    saveFile.write("Results for "+str(vectorSize)+" bits:\n\n")
    saveFile.write(str(result))

    if runAll:
        vectorSize = 1024
        result = lc.rateCalculator(vectorSize,n_iterations,step,runMean)
        saveFile.write("\n\n\nResults for "+str(vectorSize)+" bits:\n\n")
        saveFile.write(str(result))

        vectorSize = 8192
        result = lc.rateCalculator(vectorSize,n_iterations,step,runMean)
        saveFile.write("\n\n\nResults for "+str(vectorSize)+" bits:\n\n")
        saveFile.write(str(result))

        vectorSize = 16384
        result = lc.rateCalculator(vectorSize,n_iterations,step,runMean)
        saveFile.write("\n\n\nResults for "+str(vectorSize)+" bits:\n\n")
        saveFile.write(str(result))