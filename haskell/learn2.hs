-- Multiplies a string
duplicate :: String -> Int -> String
duplicate string n = concat $ replicate n string

-- replaces one char by a string
replace :: Char -> String -> String -> String
replace c new string =
  concatMap (change c new) string
  where
      change c new x
          | x == c = new
          | otherwise = x:[] -- "x"



data BinTree a = Empty
    | Node a (BinTree a) (BinTree a)


treeFromList :: Ord a => [a] -> BinTree a
treeFromList [] = Empty
treeFromList (top:rest) = Node top
    (treeFromList (filter (> top) rest))
    (treeFromList (filter (<= top) rest))

-- declare BinTree a to be an instance of Show
-- instance (Show a) => Show (BinTree a) where
--   -- will start by a '<' before the root
--   -- and put a : a begining of line
--   show t = "< " ++ replace '\n' "\n: " (treeshow "" t)
--     where
--     -- treeshow pref Tree
--     --   shows a tree and starts each line with pref
--     -- We don't display the Empty tree
--     treeshow pref Empty = ""
--     -- Leaf
--     treeshow pref (Node x Empty Empty) =
--                   (pshow pref x)

--     -- Right branch is empty
--     treeshow pref (Node x left Empty) =
--                   (pshow pref x) ++ "\n" ++
--                   (showSon pref "`--" "   " left)

--     -- Left branch is empty
--     treeshow pref (Node x Empty right) =
--                   (pshow pref x) ++ "\n" ++
--                   (showSon pref "`--" "   " right)

--     -- Tree with left and right children non empty
--     treeshow pref (Node x left right) =
--                   (showSon pref "|--" "|  " left) ++ "\n" ++
--                   (showSon pref "`--" "   " right)

--     -- shows a tree using some prefixes to make it nice
--     showSon pref before next t =
--                   pref ++ before ++ treeshow (pref ++ next) t

--     -- pshow replaces "\n" by "\n"++pref
--     pshow pref x = replace '\n' ("\n"++pref) (show x)

instance (Show a) => Show (BinTree a) where
    show t = (treeshow 0 t) where

        -- Don't show empty trees
        treeshow indent Empty = ""

        -- Final Leaf
        -- treeshow indent (Node val Empty Empty) = show val

        -- With Leaves
        treeshow indent (Node val left right) = "\n" ++ (duplicate " " indent) ++ show val ++ treeshow (indent + 2) left ++ treeshow (indent + 2) right



-- take all element of a BinTree
-- up to some depth
treeTakeDepth _ Empty = Empty
treeTakeDepth 0 _     = Empty
treeTakeDepth n (Node x left right) = let
    nl = treeTakeDepth (n-1) left
    nr = treeTakeDepth (n-1) right
    in
        Node x nl nr


-- Grabs the left side of the tree
treeLeft :: BinTree a -> BinTree a
treeLeft Empty = Empty
treeLeft (Node val left right) = left

-- Grabs the right side of the tree
treeRight :: BinTree a -> BinTree a
treeRight Empty = Empty
treeRight (Node val left right) = right

-- Grabs the value of the top node of the tree
-- Grabs the right side of the tree
treeVal :: BinTree a -> a
treeVal (Node val left right) = val



-- Apply a function to each node in a BinTree
treeMap :: (a -> b) -> BinTree a -> BinTree b
treeMap func Empty = Empty
treeMap func (Node val left right) =
    (Node $ func val)
    (treeMap func left)
    (treeMap func right)

-- treeFilter :: (a -> Bool) -> BinTree a -> BinTree a
-- treeFilter func (Node val Empty Empty) = if func val then (Node val) Empty Empty else Empty
-- treeFilter func (Node val left Empty) =
--     if func val
--         then (Node val) left Empty
--         else (Node (treeVal left)) (treeLeft left) (treeRight left)
-- treeFilter func (Node val Empty right) =
--     if func val
--         then (Node val) Empty right
--         else (Node (treeVal right)) (treeLeft right) (treeRight right)
-- treeFilter val left right =
--     if func val
--         then (Node val) left right
--         else (Node (treeVal right)) (treeLeft right) (treeRight right)


nullTree = Node 0 nullTree Empty


main :: IO()
main = do
    -- print $ treeFromList [1, 7, 5, 8, 1]
    -- print $ treeTakeDepth 4 nullTree
    print $ (treeFromList [4, 2, 3, 1])
    print $ treeMap (*2) (treeFromList [4, 2, 3, 1])
    print $ treeMap (\x -> if even x then x else 0) (treeFromList [4, 2, 3, 1])
    -- print $ treeFilter even (treeFromList [4, 2, 3, 1])


