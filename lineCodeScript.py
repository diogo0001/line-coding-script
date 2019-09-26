import lineCodeFunctions as lc

vectorSize = 16  # must be pair
step = 0.01

bits = lc.bitsGen(vectorSize)
bits = [1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1]

print(bits)

code= lc.unipolarNRZ(bits, step, True) # True to plot graphics
print("unipolarNRZ",code)

code = lc.unipolarRZ(bits, step, True) 
print("unipolarRZ",code)

code = lc.bipolarNRZ(bits, step, True) 
print("bipolarNRZ",code)

code = lc.bipolarRZ(bits, step, True) 
print("bipolarRZ",code)

code = lc.NRZSpace(bits, step, True) 
print("NRZSpace",code)

code = lc.manchester(bits, step, True) 
print("manchester",code)

code = lc.hdb3(bits, step,  True) 
print("hdb3",code)

code = lc.polarQuatNRZ(bits, step, True) 
print("polarQuatNRZ",code)

code = lc.twob1q(bits, step, True) 
print("twob1q",code)

