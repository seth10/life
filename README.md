# life
![life](https://user-images.githubusercontent.com/5026621/30190700-fa897bce-9409-11e7-9803-e2c907c0ea9c.gif)
(note the simulation was limited to 100 iteration for the sake of the .gif filesize)

Six years ago (September 2011), I needed a science fair topic. Having recently been introduced to and fascinated by John Conway's Game of Life, I formulated a hypothesis along the lines of "There exists an optimal initial population density to maximize generations until stabilization in John Conway's Game of Life." I decided to revisit this project now. You can read more about The Game of Life [here](http://web.stanford.edu/~cdebs/GameOfLife/), or use a simple online simulator [here](https://bitstorm.org/gameoflife/). Different branches off this idea and implementation decisions are given their own file, detailed below.

## ncurses.py
This was my first implementation in the revival of this project. It runs a simulation of The Game of Life and displays each iteration on screen. The grid size is a constant which may be adjusted, as is the character which is printed for "living" cells. The time each iteration is shown before the next is specified in seconds by `DELAY`. You can also set a timeout in the form of `MAX_ITERATIONS`. This program uses the `curses` library to draw over the screen instead of printing many, many lines. Be sure your terminal is at least `SIZE`+2 lines high. When the simulation completes you may press Enter to run another, or any other key to quit.

## small.py
This is a trimmed down version of the above. It cuts out all of the UI code (besides a single `print` statement) to focus on the clarity and readability of the core logic. `make2DList` is a helper method which accept arguments for the height and width of the 2D list (or array, if you prefer) to create, and a function to generate the value for each element. This last parameter is optional, by default it will simple result in an array full of `False`. `iterate` accepts a game state in the form of a 2D list and returns the following generation. `simulate` will, given a grid size and percent of cells to be initially alive, randomly generate and simulate a game of life. Note this fraction should be between 0 and 1, not 0 to 100. The function will return `False` if the population was eradicated, or `True` if it stabilized in a cycle of repeated iterations. If executed as `__main__`, it will run a hundred-thousand trials on each grid size 5x5 through 9x9, and each starting population density 0.1 through 0.9, and print the percentage of simulations that stabilized (did not die out).

## ninty_percent.py
<img alt="A 2D bar graph titled: Stabilization (not eradication) at 90% initial population" src="https://user-images.githubusercontent.com/5026621/30225545-d695bc0e-94a0-11e7-8bd3-785f9bdee5fa.png" width="100%">
This program focuses on the question of "Do any simulations actually survive at 90% [initial population density]?" Looking at the previous programs I almost always saw a 0% survival at 90% of cells initially populated. (Note 100% is a trivial case as all cells will die of overcrowding in one generation.) This program will run through simulations at grid sizes 5x5 by 9x9 with a 90% starting percentage of cells alive. Once it completes running ten-thousand trials at each grid size, it uses matplotlib to display a bar chart with the percentage of simulations that survived on each grid size. It took about twenty seconds to run the fifty-thousand simulations on my computer.

## science.py
<img alt="A 3D bar graph titled: Initial cell population and grid size vs generations until stabilization" src="https://user-images.githubusercontent.com/5026621/30236053-bb1ecdbe-94df-11e7-9c5a-9085b8ecac72.png" width="100%">
I wrote this program really because I was thinking of ways to visualize data related to this project and just wanted to make a 3D bar chart, because it looks cool.

## tkinter.py
<img alt="A window using Tk to render an animation of The Game of Life" src="https://user-images.githubusercontent.com/5026621/30236283-38655032-94e4-11e7-9c11-163bfd85cf9c.gif" width="40%"><img alt="A dialog box stating: Stable after 102 generations with a cycle of length 1" src="https://user-images.githubusercontent.com/5026621/30236287-4c126656-94e4-11e7-85d1-9a3884ab4d5e.png" width="60%">
I was having some trouble with matplotlib on Windows; so, knowing Tk is cross-platform, I wanted to use the `tkinter` module included in Python to visualize the simulations.

## update.py
<img alt="A live-updating 2D bar graph titled: Initial population vs generation count" src="https://user-images.githubusercontent.com/5026621/30242311-03b56aa6-9562-11e7-8bef-2f6650cbaf05.gif" width="100%">
The aim of the program is to continually run more simulations and collect more data to move the bars to more accurate positions.
