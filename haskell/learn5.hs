
-- Import * into global scope
import Data.Map.Strict

-- Import specific things into global
import Data.Map.Lazy (filter, foldr)

-- Import everything EXCEPT X into global
import Data.Map.Lazy hiding (valid, showTree)

-- Import as itself
import qualified Data.Map.Lazy

-- Import as name
import qualified Data.Map.Lazy as Map



-- Import list methods that can run on more than just Int
import Data.List (genericLength, genericTake, genericIndex)


import Geometry


main = do print $ cuboidVolume
