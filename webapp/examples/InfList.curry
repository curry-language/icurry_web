-- An infinite computation: select the last element of an infinite list

last [x] = x
last (_:xs@(_:_)) = last xs

trueList :: [Bool]
trueList = True : trueList

-- infinitely many values: use option --interactive
main :: Bool
main = last trueList
