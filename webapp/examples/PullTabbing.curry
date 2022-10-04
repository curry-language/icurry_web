-- This example demonstrates the effect of pull tabbing to handle
-- non-deterministic computations. In contrast to backtracking (as in Prolog),
-- non-deterministic choices are rexplicitly epresented as choice nodes ("?").
-- If a choice occurs deeply in an expression, pull tabbing
-- moves the choice to the top and duplicates the spine
-- before splitting the computations into two tasks.

not False = True
not True  = False

solve True = True

aBool = False ? True

main = not (not (not (solve aBool)))
