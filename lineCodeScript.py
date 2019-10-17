import lineCodeFunctions as lc
import json

vectorSize = 16000       # Must be pair
step = 0.01           # Time for each symbol
n_iterations = 1

result = lc.rateErrorCalculatorScript(vectorSize,n_iterations,step)

# for x in result:
#   print(result[x]["BipolarNRZ_noise"])

# result_json = json.dumps(result,indent=4)
# print(result_json)

with open("Results.json", "w") as write_file:
    json.dump(result, write_file,indent=4)

# with open('Results.json',"r") as json_file:
#     data = json.load(json_file)

# print(data)

