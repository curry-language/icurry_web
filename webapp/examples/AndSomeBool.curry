-- A simple example where a shared non-deterministic value is used twice.

-- Boolean conjunction:
and False _ = False
and True  x = x

-- Some Boolean value:
aBool = False ? True

-- Share the argument of the operation `and`:
andSelf x = and x x

-- Evaluate an expression with a shared non-deterministic value:
main = andSelf aBool
