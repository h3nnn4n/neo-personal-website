---
title: "Smart Panda - A Tetris Playground for AIs"
date: 2019-03-04
tags: ["artificial intelligence", "tetris"]
draft: false
---

Smart Panda is a simple Tetris Playground intended for use with Artificial Intelligences. That is,
the intended use of Smart Panda is as a Tetris engine to explore and apply some Artificial Intelligence
concepts to Tetris. The core of Smart Panda is written in [rust](https://www.rust-lang.org/), compiled to
[wasm](https://developer.mozilla.org/en-US/docs/WebAssembly) using
[wasm-pack](https://rustwasm.github.io/wasm-pack/) and
[wasm-bindgen](https://rustwasm.github.io/wasm-bindgen/). What you see happening on the browser
right now is controlled with JavaScript. That is, the heavy lifting is made in rust and javascript
does some glue logic and calls the update events from Smart Panda. This (should) allow for
some pretty amazing thing to be made here ;)

The goal is to implement a simple agent that can play the game. In the past, I made one using
a [Game Boy Emulator](https://github.com/h3nnn4n/garapa/) with a
[Genetic Algorithm](https://github.com/h3nnn4n/garapa/tree/gabate/)
and a paper was published about it with the title
_Playing the Original Game Boy Tetris Using a Real Coded Genetic Algorithm_, in case you are interested.
So now, I plan to experiment more using simpler methods (I suspect that they might be enough).
Running it in the browser should allow easier exploration thanks to a more accessible
interface and ease of implementation. With the rust core speed should not be an issue.
And finally, it allows for easier visualization and divulgation. No more need to compile
C code and get hold of a shady Tetris rom.

The project as a whole still is a Work In Progress. It has some unpolished parts. Some bad code here and there.
One of the main goals of the project was for me to learn more about JavaScript and its tools. The other
main goal was to make an Tetris playing agent that is at least half decent.

Below you should be seeing a Tetris game being played with some pretty bad moves. By default
a learning agent plays it. A Monte Carlo search looks for which features are good/bad and
tries to learn from it. As of the time of writing this it can learn a bit but still is a
very bad bot. There is also an option of selecting a Random Agent, which just play random moves.
It also plays slower, so it is easier to see what is going on.

<iframe src="{% static 'external/smart-panda/index.html' %}" width="700" height="600" frameBorder="0"></iframe>

The information to the right of the tetris box is contains some useful information.
`lines_cleared` shows how many lines have been cleared during the current game and `best`
shows the best result so far. For each strategy that the agent tries it plays 10 games. The
average number of lines cleared during these games is used to score how good/bad it is.
The best mean is shown as `best_mean`, while `current_mean` shows the mean score
of the current iteration. The two next lines shows the weights of each feature.
The top line is best strategy so far while the bottom one is the strategy being
tried. Finally, the last lines shows the features and its respective values for the current
board status.

The tetris playing agent is guided by the feature functions multiplied by some weight summed together.
This number always is being optimized. A higher number (should) mean a better move.
This means that the agent is composed of two optimizers. One tries to learn the best
strategy while the other tries to find the best move using the current strategy.

Note: If you are seeing nothing than this means that your browser does not support WASM :(
Note2: If you are on mobile the page will probably look like crap :(
