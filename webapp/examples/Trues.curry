-- Example to show a computation with a cyclic structure

head (x:_) = x

not True = False
not False = True

-- Compute with a first element of a cyclic list of True values:
main = let trues = True : trues in not (head trues) 
