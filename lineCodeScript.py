import lineCodeFunctions as lc

vectorSize = 16  # must be pair
Ts = 1
step = 0.01

bits = lc.bitsGen(vectorSize)
# bits = [1,0,1,1,0,0,0,1]

print(bits)

code= lc.unipolarNRZ(bits, step, Ts, True) # True to plot graphics
print("unipolarNRZ",code)

code = lc.unipolarRZ(bits, step, Ts, True) 
print("unipolarRZ",code)

code = lc.bipolarNRZ(bits, step, Ts, True) 
print("bipolarNRZ",code)

code = lc.bipolarRZ(bits, step, Ts, True) 
print("bipolarRZ",code)

code = lc.polarQuatNRZ(bits, step, Ts, True) 
print("polarQuatNRZ",code)

code = lc.NRZSpace(bits, step, Ts, True) 
print("NRZSpace",code)

code = lc.manchester(bits, step, Ts, True) 
print("manchester",code)

code = lc.hdb3(bits, step, Ts, True) 
print("hdb3",code)

code = lc.twob1q(bits, step, Ts, True) 
print("twob1q",code)

