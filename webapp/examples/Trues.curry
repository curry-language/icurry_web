head (x:_) = x

not True = False
not False = True

main = let trues = True : trues in not (head trues) 
