# balls-engine
Python to solve crossing out balls game

Rules of the game are very simple. 

There is a square board of balls:
  O O O
  O O O
  O O O
and two players.

In every turn players cross out balls in row or column:
move 1:
  X X O
  O O O
  O O O
move 2:
  X X X
  O O X
  O O X
etc.

It is possible to cross out over crossed out balls:
  O X O    X X X
  O O O -> O O O
  O O O    O O O
  
Who cross out last ball, loses.


 
