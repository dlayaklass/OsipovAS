module Main where

import Basics
import Recursion
import Patterns
import HigherOrder
import Types
import Practice

main :: IO ()
main = do
    putStrLn "=== Демонстрация работы функций ==="
    
    putStrLn "\n--- Базовые функции ---"
    print $ square 5
    print $ grade 85
    
    putStrLn "\n--- Рекурсия ---"
    print $ factorial 5
    print $ sumList [1, 2, 3, 4, 5]
    print $ fibonacci 7
    
    putStrLn "\n--- Pattern matching ---"
    print $ addVectors (1, 2) (3, 4)
    print $ first (10, 20, 30)
    print $ describeList [1, 2, 3]
    
    putStrLn "\n--- Функции высшего порядка ---"
    print $ map' square [1, 2, 3, 4]
    print $ filter' even [1, 2, 3, 4, 5, 6]
    print $ foldl' (+) 0 [1, 2, 3, 4, 5]
    
    putStrLn "\n--- Алгебраические типы ---"
    print $ distance (Point 0 0) (Point 3 4)
    print $ isWeekend Saturday
    print $ isWeekend Monday
    
    putStrLn "\n--- Практические задания ---"
    print $ countEven [1, 2, 3, 4, 5, 6]
    print $ positiveSquares [-2, -1, 0, 1, 2, 3]
    print $ bubbleSort [3, 1, 4, 1, 5, 9, 2, 6]

