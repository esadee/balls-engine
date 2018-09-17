# balls-engine
Python to solve crossing out balls game

Rules of the game are very simple. 

There is a square board of balls:<br/>

  O O O<br/>
  O O O<br/>
  O O O<br/>
and two players.

In every turn players cross out balls in row or column:<br/>
move 1:<br/>
  X X O<br/>
  O O O<br/>
  O O O<br/>
move 2:<br/>
  X X X<br/>
  O O X<br/>
  O O X<br/>
etc.

It is possible to cross out over crossed out balls:<br/>
  O X O -> X X X<br/>
  O O O -> O O O<br/>
  O O O -> O O O<br/>
  
Who cross out last ball, loses.
