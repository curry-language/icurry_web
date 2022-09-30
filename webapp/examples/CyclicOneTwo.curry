-- Example to show a computation with a cyclic structure of two elements

-- The infinite list of 1,2,1,2,...
oneTwo :: [Int]
oneTwo = let x = 1 : y
             y = 2 : x
         in x

head (x:_) = x

tail (_:xs) = xs

-- Compute the second element of a cyclic list:
main = head (tail oneTwo)
