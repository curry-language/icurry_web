-- An example for computing with nested patterns and cyclic structures

zip               :: [a] -> [b] -> [(a,b)]
zip []     _      = []
zip (_:_)  []     = []
zip (x:xs) (y:ys) = (x,y) : zip xs ys

ones :: [Int]
ones = let xs = 1 : xs in xs

-- Zip a finite with an infinite list:
main :: [(Int,Int)]
main = normalForm (zip [1,2] ones)
