-- the classical example from the KiCS2 paper:
xor False y = y
xor True  y = not y

not False = True
not True  = False

xorSelf x = xor x x

aBool = False ? True

main = xorSelf aBool
