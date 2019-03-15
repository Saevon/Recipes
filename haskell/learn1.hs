{-# LANGUAGE PatternGuards #-}

-- Needed for hsdev
module Main where


main :: IO()
main = do
    let input = [1, 2, 3, 12, 4, 3]
    print $ sumEven input
    -- print $ squareEven input
    print $ sumEven' input
    -- print $ sumEven'' input
    -- print $ sumeven''' input
    -- print $ square 2

square x = x * x

-- Function Composition
even' :: Integral a => a -> Bool
even' = (== 0) . (`mod` 2)



-- Functional (Reduce + filter) approach
sumEven :: Integral a => [a] -> a
sumEven items = foldl (+) 0 . filter even'
    -- This isn't necessary (if you drop the items argument then this
    -- returns a function, which applies to the first argument given
    $ items




squareEven :: Integral a => [a] -> a
squareEven = sumEven . map (^2)


-- Recursive integration, using guards?
sumEven' :: Integral a => [a] -> a
sumEven' items
    | ((length items) == 0) = 0
    | otherwise = ((\x -> if even x then x else 0) (head items)) + sumEven' (tail items)


-- Recursive integration, using non-functional approach
sumEven'' :: [Integer] -> Integer
sumEven'' items =
    if length items == 0 then 0 else
        let item = head items
            rest = tail items
        in if even item
            then item + sumEven'' rest
            else sumEven'' rest


-- Recursive integration, using ternary (and unpacking)
sumEven''' :: [Integer] -> Integer
sumEven''' [] = 0
sumEven''' (item:rest) = if even item
    then item + sumEven''' rest
    else sumEven''' rest


-- Recursive, with guards
sumEven'''' :: [Integer] -> Integer
sumEven'''' [] = 0
sumEven'''' (item:rest)
    | even item = item + sumEven'''' rest
    | otherwise = sumEven'''' rest






