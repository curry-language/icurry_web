-- Testing infinitely many results

aBool :: Bool
aBool = False ? True

last [x] = x
last (_:xs@(_:_)) = last xs

aBoolList :: [Bool]
aBoolList = True : aBoolList

-- infinitely many values: use option --interactive
main :: Bool
main = last aBoolList

-- > icurry -i -m main --graphsvg=BL BoolList
