import sys
sys.path.insert(1, '../src')

import TestParser
import TestGame

if __name__ == "__main__":
   TestParser.test()
   print("[TEST] Tests on parser successful!")

   TestGame.test()
   print("[TEST] Tests on game successful!")