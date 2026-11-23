# best_path
HOW TO PLAY

Use the itch.io page for a simple way to play the game.

itch.io page = https://jplackal.itch.io/best-path

Or use the source code to run it from your computer.

source code = https://github.com/jplackal/best_path/blob/main/main.py

You need pygame and asyncio.

HOW IT WORKS

It works by slowly searching through each possible option using units of time that slowly increase. Each connection between points has a number that represents how much time it takes to travel through it. All of the possible paths grow in a tree that is stored in a big list. To navigate through this tree, I use a recursive function that explores each branch and keeps track of the different paths. When it reaches the end_id, it saves the path it took and displays it on the screen. The tree also gets drawn while the search is happening so you can see how the paths expand.

To make this, I came up with my own ideas and system for how the pathfinding would work. I wanted to make something that could show all the different possibilities instead of just instantly giving the answer. This was also the first time I had ever used recursive functions. I had to figure out how to use recursion to navigate through a list that contains more lists inside it, and that ended up being one of the most important parts of the project. I also had to spend some time figuring out how to make the tree draw corectly while it was searching.
