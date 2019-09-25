import lineCodeFunctions as lc

vectorSize = 10
Ts = 1
step = 0.01

bits = lc.bitsGen(vectorSize)
# bits = [1,0,1,1,0,0,1,0]
print(bits)

xt = lc.unipolarNRZ(bits, step, Ts, True)
