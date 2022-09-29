-- A simple example for sharing in lazy functional computations

-- Boolean conjunction:
and :: Bool -> Bool -> Bool
and False _ = False
and True  x = x

-- Boolean negation:
not :: Bool -> Bool
not False = True
not True  = False

-- Share an argument:
andSelf :: Bool -> Bool
andSelf x = and x x

-- Evaluate an expression with a shared computation:
main = andSelf (not False)
