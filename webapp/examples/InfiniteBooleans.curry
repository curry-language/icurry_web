-- An example to compute infinitely many results

aBool :: Bool
aBool = False ? True

aBoolList :: [Bool]
aBoolList = []
aBoolList = aBool : aBoolList

-- Compute arbitrary lists of Booleans, i.e., [], [False], [True],...
main :: [Bool]
main = normalForm aBoolList
