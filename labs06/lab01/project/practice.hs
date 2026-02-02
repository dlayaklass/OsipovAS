module Practice where

countEven :: [Int] -> Int
countEven [] = 0
countEven (x:xs)
    | even x    = 1 + countEven xs
    | otherwise = countEven xs

positiveSquares :: [Int] -> [Int]
positiveSquares xs = [x*x | x <- xs, x > 0]

bubbleSort :: [Int] -> [Int]
bubbleSort [] = []
bubbleSort [x] = [x]
bubbleSort xs = if xs == bubblePass xs then xs else bubbleSort (bubblePass xs)
    where
        bubblePass [] = []
        bubblePass [x] = [x]
        bubblePass (x:y:ys)
            | x > y     = y : bubblePass (x:ys)
            | otherwise = x : bubblePass (y:ys)

