#!/usr/bin/env haskell
import Prelude;

main :: IO()
main = do
    -- putStrLn $ concat' "What is 2 + 2?" $ formatString $ 1 + 2
    putStrLn $ concat' "a" "b"
    -- Infix operator
    putStrLn $ "a" `concat'` "a"

    -- List comprehension
    putStrLn $ [a ++ "-" | a <- ["a", "b"]] !! 0


concat' :: String -> String -> String
concat' x y =  x ++ y
data Superb = A Int | B Int;


-- compose' :: (Int -> Int) -> Int -> (Int ->Int)
-- compose' f g = \x -> f . g $ x

iterate' :: (a -> a) -> a -> [a]
iterate' f x = x : (iterate' f  . f $ x)


-- iterate' :: (a -> a) -> a -> [a]
-- iterate' f (top:x) = f top : iterate' f x






-- -- Syntax TODO:

-- -- Lambda
-- compose' f g = \x -> f . g $ x

-- -- Infix Functions?
-- "a" `compose'` "b"

-- -- Only classes can start with A-Z?
