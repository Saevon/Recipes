data BalTree a = Empty
    | TwoNode (BalTree a) a (BalTree a) a (BalTree a)
    | OneNode (BalTree a) a (BalTree a)
    | TwoLeaf a a
    | OneLeaf a
        -- deriving(Show)


-- declare BinTree a to be an instance of Show
instance (Show a) => Show (BalTree a) where
  -- will start by a '<' before the root
  -- and put a : a begining of line
  show t = "< " ++ replace '\n' "\n: " (treeshow "" t)
    where
    -- treeshow pref Tree
    --   shows a tree and starts each line with pref

    -- We don't display the Empty tree
    treeshow pref Empty = ""

    -- Leaves
    treeshow pref (OneLeaf leftVal) =
        (pshow pref leftVal)

    treeshow pref (TwoLeaf leftVal rightVal) =
        (pshow pref leftVal)
        ++ "\n" ++
        (pshow pref rightVal)

    -- -- Nodes
    treeshow pref (OneNode leftTree middle rightTree) =
        (pshow pref middle)
        ++ "\n" ++
        (showSon pref "|--" "|  " leftTree)
        ++ "\n" ++
        (showSon pref "`--" "   " rightTree)

    treeshow pref (TwoNode leftTree leftVal middleTree rightVal rightTree) =
        (pshow pref leftVal)
        ++ "\n" ++
        (showSon pref "`--" "   " rightTree)
        ++ "\n" ++
        (showSon pref "|--" "|  " leftTree)
        ++ "\n" ++
        (pshow pref rightVal)
        ++ "\n" ++
        (showSon pref "|--" "|  " middleTree)
        ++ "\n" ++
        (showSon pref "`--" "   " rightTree)


    -- shows a tree using some prefixes to make it nice
    showSon pref before next t =
                  pref ++ before ++ treeshow (pref ++ next) t

    -- pshow replaces "\n" by "\n"++pref
    pshow :: String -> a -> w -> IO()
    pshow pref x = replace '\n' ("\n"++pref) (show x)

    -- replaces one char by another string
    replace c new string =
      concatMap (change c new) string
      where
          change c new x
              | x == c = new
              | otherwise = x:[] -- "x"



main :: IO()
main = do
    -- Creation
    print $ (OneNode Empty 10 Empty)

    -- Deletion
