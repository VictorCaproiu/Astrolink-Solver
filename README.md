# AstrolinkSolver

As a fan of puzzles, I’m always looking for new challenges. When I discovered the game Astrolink, I was hooked by its increasingly difficult levels. Eventually, I found myself struggling with the hardest levels, realizing the limits of what I could solve by hand.

<img src="media\AstroinkPuzzle.jpg" alt="" width="400"/> 

Setup for level 32 (the one that broke me)

Instead of admitting defeat, I did what any reasonable person would do: I wrote a Python backtracking algorithm to solve the puzzles for me. Take that, human brain limitations! Now I can watch my code do the heavy lifting.

<img src="media\AstrolinkSolverDemo.gif" alt="" width="400"/>

## Performance considerations

Initial tests using the unoptimised backtracking algorithm showed poor performance, taking close to an hour to solve level 32.

In order to improve the runtime the algorithm checks at every step for "impossible patterns" (inaccessible gaps of one or two squares) based on which it backtracks immediatly. This shortened the runtime massivlely:

| Level Number   | Difficulty | Solve Time | Missing Pieces |
|:--------------:|:----------:|:----------:|:--------------:|
| No.1           |  Starter   |    01s     |       3        |
| No.32          |  Master    |    17s     |       8        |
| No.37          |  Wizard    |  03m:09s    |      10        |
