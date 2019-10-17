import lineCodeFunctions as lc

vectorSize = 16        # Must be pair
step = 0.01              # Time for each symbol

n_iterations = 1
result = lc.rateErrorCalculatorScript(vectorSize,n_iterations,step)

# saveFile = open("Results_mean.txt","w")
# saveFile.write("Results for "+str(vectorSize)+" bits:\n\n")
# saveFile.write(str(result))

# print(lc.gen())
