removeNonUppercase :: String -> String
removeNonUppercase string = [x | x <- string, x `elem` ['A','B'..'Z']]


thrd :: (a, b, c) -> c
thrd (a, b, c) = c
  -- print $ [point | point <- [ (a, b, 24 - a - b) | a <- [1..10], b <- [1..10]], point!!0^2 + point!!1^2 == point!!2^2]


-- Returns all possibilities of an Enum
-- fullEnum :: Bounded a => Enum a => a -> [a]
-- fullEnum val = [(minBound :: a)..(maxBound :: a)]
capital :: String -> String
capital "" = "Empty Strings don't have a first letter"
capital all@(first:_) = "The first letter of " ++ all ++ " is " ++ [first]


-- Recursive Max function
max' :: Ord a => [a] -> a
max' [] = error "No Max Possible"
max' [one] = one
max' (first:rest)
  | first > curMax = first
  | otherwise      = curMax
  where curMax = max' rest

replicate' :: (Num a, Ord a) => a -> b -> [b]
replicate' n val
  | n <= 0    = []
  | otherwise = val:replicate' (n - 1) val

quicksort :: (Ord a) => [a] -> [a]
quicksort [] = []
quicksort (top:rest) = left ++ [top] ++ right where
  left = quicksort [val | val <- rest, val <= top]
  right = quicksort [val | val <- rest, val > top]

oddSquares = map fst (takeWhile (\(x, val) -> val<10000) (map (\x -> (x, x^2)) [1..]))

collatz :: Integer -> [Integer]
collatz 1 = [1]
collatz n = [n] ++ (collatz next) where
  next = if (n `mod` 2) /= 0 then (n * 3 + 1)
    else (n `div` 2)


main :: IO()
main = do
  print $ removeNonUppercase "IdontLIKEFROGS"
  print $ ([(a, b, c) | a <- [1..10], b <- [1..10], c <- [1..10], a + b + c == 24, a^2 + b^2 == c^2] :: [(Int,Int,Int)])
  -- print $ (1, 2, 3) !! 2
  print $ (read "123" :: Int)
  print $ (maxBound :: Int)
  print $ (maxBound :: Bool)
  print $ (maxBound ::  Bool)
  print $ capital "Dracula"
  print $ max' [1,4,6,7,3,6,8,3]
  print $ replicate' 10 "a"
  print $ quicksort [1,2,4,5,2,2,6,8,90,2,5]
  -- print $ oddSquares
  print $ length . filter (\x -> length x > 15) . map collatz $ [1..100]
  print $ length . filter ((> 15) . length) . map collatz $ [1..100]

  -- What I want to do in haskell (note the . operator is the bit I want to replace)
  -- Essentially it lets me swap function order
  -- print $ map collatz
  --   . filter (length . (>15))
  --   -- How many matched this criteria
  --   . length
  --   -- The input would go here (like normal?) or if it could be the first thing...
  --   $ [1..100]

  length . filter ((> 15) . length) . map collatz $ [1..100]
  -- print $ scanl (+) [1, 0, 0, 4, 0, 1, 2] 0

  -- An array of operations, each of which gets run on the 4
  print $ map ($ 2) [(4+), (10*), (^2), sqrt]









