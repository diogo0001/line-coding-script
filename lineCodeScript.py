import lineCodeFunctions as lc

vectorSize = 32  # must be pair
Ts = 1
step = 0.05

bits = lc.bitsGen(vectorSize)
# bits = [1,0,1,1,0,0,0,1]

print(bits)

# xt= lc.unipolarNRZ(bits, step, Ts, True) # True to plot graphics

# xt = lc.unipolarRZ(bits, step, Ts, True) 

# xt = lc.bipolarNRZ(bits, step, Ts, True) 

# xt = lc.bipolarRZ(bits, step, Ts, True) 

# xt = lc.polarQuatNRZ(bits, step, Ts, True) 

# xt = lc.NRZSpace(bits, step, Ts, True) 

# xt = lc.manchester(bits, step, Ts, True) 

# xt = lc.hdb3(bits, step, Ts, True) 

xt = lc.twob1q(bits, step, Ts, True) 

print(xt)

