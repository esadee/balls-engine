# balls-engine
Python to solve crossing out balls game

Rules of the game are very simple. 

There is a square board of balls:<br/>

  <code>O O O</code><br/>
  <code>O O O</code><br/>
  <code>O O O</code><br/>
  
and two players.

In every turn players cross out balls in row or column:<br/>
move 1:<br/>

  <code>X X O</code><br/>
  <code>O O O</code><br/>
  <code>O O O</code><br/>

move 2:<br/>
  <code>X X X</code><br/>
  <code>O O X</code><br/>
  <code>O O X</code><br/>
etc.

It is possible to cross out over crossed out balls:<br/>
  <code>O X O -> X X X</code> <br/>
  <code>O O O -> O O O</code> <br/>
  <code>O O O -> O O O</code> <br/>
  
Who crosses out last ball, loses.
