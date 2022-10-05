-- A simple example where a shared non-deterministic expression is used twice.

-- Boolean conjunction:
and False _ = False
and True  x = x

-- Boolean negation:
not False = True
not True  = False

-- Some Boolean value:
aBool = False ? True

-- Share the negated argument in the operation `and`:
andNotSelf x = and (not x) (not x)

-- Evaluate an expression with a shared non-deterministic value:
main = andNotSelf aBool
