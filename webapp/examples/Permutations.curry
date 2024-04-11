-- Example for non-deterministic programming: computing permutations

-- Non-deterministic insertion into a list
ndinsert x xs     = x:xs
ndinsert x (y:ys) = y : ndinsert x ys

-- Some permutation of a list
perm []     = []
perm (x:xs) = ndinsert x (perm xs)

-- Compute the permutations of a given list (requires 127 steps)
main :: [Int]
main = normalForm (perm [1,2])
