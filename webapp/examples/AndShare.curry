-- A simple example for sharing in lazy functional computations

-- Boolean conjunction:
and False _ = False
and True  x = x

-- Boolean negation:
not False = True
not True  = False

-- Share the argument of the operation `and`:
andSelf x = and x x

-- Evaluate an expression with a shared computation:
main = andSelf (not False)
