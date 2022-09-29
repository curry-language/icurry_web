-- The classical example from the KiCS2 paper which demonstrates
-- the necessity to identify different choice nodes, see
-- http://dx.doi.org/10.1007/978-3-642-22531-4_1

aBool = False ? True

not False = True
not True  = False

xor False y = y
xor True  y = not y

xorSelf x = xor x x

main = xorSelf aBool
